### File: backend/app/models/player.py

"""
backend/app/models/player.py
STEP: Player Data Models
Defines player profile, authentication, and session tracking in PostgreSQL.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base


class Player(Base):
    """Player account and profile"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    display_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Stats
    total_games = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    oracles_defeated = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    sessions = relationship("PlayerSession", back_populates="player", cascade="all, delete-orphan")
    game_states = relationship("GameState", back_populates="player", cascade="all, delete-orphan")


class PlayerSession(Base):
    """Active player sessions for JWT management"""
    __tablename__ = "player_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    token_jti = Column(String(255), unique=True, nullable=False, index=True)
    
    # Session info
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    player = relationship("Player", back_populates="sessions")
