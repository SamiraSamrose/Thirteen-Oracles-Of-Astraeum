### File: frontend/src/types/index.ts

/**
 * frontend/src/types/index.ts
 * STEP: TypeScript Type Definitions
 * Defines interfaces for game state, oracles, armies, etc.
 */

export interface Player {
  id: number
  username: string
  email: string
  display_name: string
  total_games: number
  games_won: number
  oracles_defeated: number
}

export interface Oracle {
  id: number
  name: string
  domain: string
  title: string
  description: string
  is_defeated: boolean
  is_hostile: boolean
  current_phase: string.services.auth_service import AuthService
from app.models.player import Player

router = APIRouter()
security = HTTPBearer()


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    player_id: int
    username: str


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register new player account.
    STEP: Creates account, generates JWT, returns token.
    """
    player = await AuthService.register_player(
        db,
        request.username,
        request.email,
        request.password,
        request.display_name
    )
    
    token, _ = AuthService.create_access_token(player.id, player.username)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        player_id=player.id,
        username=player.username
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
    user_agent: str | None = Header(None)
):
    """
    Login and get access token.
    STEP: Authenticates player, creates session, returns JWT.
    """
    player, token = await AuthService.login_player(
        db,
        request.username,
        request.password,
        user_agent=user_agent
    )
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        player_id=player.id,
        username=player.username
    )


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout and invalidate session.
    STEP: Removes session from database.
    """
    await AuthService.logout_player(db, credentials.credentials)
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated player info.
    STEP: Validates token, returns player profile.
    """
    player = await AuthService.verify_session(db, credentials.credentials)
    
    return {
        "id": player.id,
        "username": player.username,
        "email": player.email,
        "display_name": player.display_name,
        "total_games": player.total_games,
        "games_won": player.games_won,
        "oracles_defeated": player.oracles_defeated
    }


async def get_current_player(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Player:
    """
    Dependency for getting current authenticated player.
    STEP: Reusable dependency for protected routes.
    """
    return await AuthService.verify_session(db, credentials.credentials)
