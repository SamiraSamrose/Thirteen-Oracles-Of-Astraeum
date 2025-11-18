### File: backend/app/services/auth_service.py

"""
backend/app/services/auth_service.py
STEP: Authentication Service
Handles user registration, login, JWT generation, and session management.
"""
import uuid
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.player import Player, PlayerSession

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication and authorization service"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plaintext password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(player_id: int, username: str) -> tuple[str, str]:
        """
        Create JWT access token with unique JTI for session tracking.
        Returns: (token, jti)
        """
        jti = str(uuid.uuid4())
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        payload = {
            "sub": str(player_id),
            "username": username,
            "jti": jti,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return token, jti
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
    
    @staticmethod
    async def register_player(
        db: AsyncSession,
        username: str,
        email: str,
        password: str,
        display_name: Optional[str] = None
    ) -> Player:
        """Register a new player"""
        # Check if username exists
        result = await db.execute(
            select(Player).where(Player.username == username)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Check if email exists
        result = await db.execute(
            select(Player).where(Player.email == email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create player
        hashed_password = AuthService.hash_password(password)
        player = Player(
            username=username,
            email=email,
            hashed_password=hashed_password,
            display_name=display_name or username
        )
        
        db.add(player)
        await db.commit()
        await db.refresh(player)
        
        return player
    
    @staticmethod
    async def login_player(
        db: AsyncSession,
        username: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> tuple[Player, str]:
        """
        Authenticate player and create session.
        Returns: (player, token)
        """
        # Find player
        result = await db.execute(
            select(Player).where(Player.username == username)
        )
        player = result.scalar_one_or_none()
        
        if not player or not AuthService.verify_password(password, player.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not player.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled"
            )
        
        # Create token and session
        token, jti = AuthService.create_access_token(player.id, player.username)
        
        session = PlayerSession(
            player_id=player.id,
            token_jti=jti,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        )
        
        player.last_login = datetime.utcnow()
        
        db.add(session)
        await db.commit()
        
        return player, token
    
    @staticmethod
    async def verify_session(db: AsyncSession, token: str) -> Player:
        """Verify JWT token and check session validity"""
        payload = AuthService.decode_token(token)
        jti = payload.get("jti")
        player_id = int(payload.get("sub"))
        
        # Check if session exists and is valid
        result = await db.execute(
            select(PlayerSession).where(
                PlayerSession.token_jti == jti,
                PlayerSession.expires_at > datetime.utcnow()
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or invalid"
            )
        
        # Update last activity
        session.last_activity = datetime.utcnow()
        await db.commit()
        
        # Get player
        result = await db.execute(
            select(Player).where(Player.id == player_id)
        )
        player = result.scalar_one_or_none()
        
        if not player or not player.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Player not found or inactive"
            )
        
        return player
    
    @staticmethod
    async def logout_player(db: AsyncSession, token: str):
        """Logout player by invalidating session"""
        payload = AuthService.decode_token(token)
        jti = payload.get("jti")
        
        result = await db.execute(
            select(PlayerSession).where(PlayerSession.token_jti == jti)
        )
        session = result.scalar_one_or_none()
        
        if session:
            await db.delete(session)
            await db.commit()
