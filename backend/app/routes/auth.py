### File: backend/app/routes/auth.py

"""
backend/app/routes/auth.py
STEP: Authentication API Routes
Handles registration, login, logout, token validation.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.services.game_service import GameService
from app.routes.auth import get_current_player
from app.models.player import Player

router = APIRouter()


class CreateGameRequest(BaseModel):
    difficulty: str = "normal"


class UseInsightRequest(BaseModel):
    question: str


@router.post("/create")
async def create_game(
    request: CreateGameRequest,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new game session.
    STEP: Initializes game state, 13 dominions, starting resources.
    """
    game_state = await GameService.create_new_game(
        db,
        player.id,
        request.difficulty
    )
    
    return {
        "game_id": game_state.id,
        "message": "Game created successfully",
        "starting_resources": {
            "weapons": game_state.weapons,
            "gold": game_state.gold,
            "insight_tokens": game_state.insight_tokens
        }
    }


@router.get("/{game_id}")
async def get_game(
    game_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete game state.
    STEP: Returns all game data including oracles, dominions, armies.
    """
    game_state = await GameService.get_game_state(db, game_id, player.id)
    
    return {
        "game_id": game_state.id,
        "current_stage": game_state.current_stage,
        "oracles_defeated": game_state.oracles_defeated,
        "resources": {
            "gold": game_state.gold,
            "insight_tokens": game_state.insight_tokens,
            "healing_draughts": game_state.healing_draughts
        },
        "inventory": {
            "weapons": game_state.weapons,
            "special_items": game_state.special_items,
            "potions": game_state.potions
        },
        "is_completed": game_state.is_completed,
        "oracles": [
            {
                "id": os.oracle.id,
                "name": os.oracle.name,
                "domain": os.oracle.domain,
                "is_defeated": os.is_defeated,
                "is_hostile": os.is_hostile,
                "current_phase": os.current_phase
            }
            for os in game_state.oracle_states
        ],
        "dominions": [
            {
                "name": ds.name,
                "oracle_name": ds.oracle_name,
                "is_controlled": ds.is_controlled,
                "is_accessible": ds.is_accessible
            }
            for ds in game_state.dominion_states
        ]
    }


@router.post("/{game_id}/save")
async def save_game(
    game_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Save current game progress.
    STEP: Persists game state to PostgreSQL.
    """
    result = await GameService.save_game_state(db, game_id, player.id)
    return result


@router.get("/{game_id}/inventory")
async def get_inventory(
    game_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Get player inventory and armies.
    STEP: Returns complete inventory with all resources.
    """
    inventory = await GameService.get_player_inventory(db, game_id, player.id)
    return inventory


@router.post("/{game_id}/insight")
async def use_insight_token(
    game_id: int,
    request: UseInsightRequest,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Use insight token for hint.
    STEP: Decrements token, triggers LLM hint generation.
    """
    result = await GameService.use_insight_token(
        db,
        game_id,
        player.id,
        request.question
    )
    return result
