### File: backend/app/routes/oracle.py

"""
backend/app/routes/oracle.py
STEP: Oracle Interaction API Routes
Handles oracle challenges, puzzles, battles, diplomacy.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.services.game_service import GameService
from app.services.puzzle_service import PuzzleService
from app.services.combat_service import CombatService
from app.routes.auth import get_current_player
from app.models.player import Player

router = APIRouter()


class SelectOracleRequest(BaseModel):
    oracle_name: str


class PuzzleSolutionRequest(BaseModel):
    oracle_state_id: int
    solution: str


class BattleActionRequest(BaseModel):
    action: str


@router.post("/challenge")
async def challenge_oracle(
    request: SelectOracleRequest,
    game_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Select oracle to challenge.
    STEP: Initiates oracle encounter, sets phase to exploration.
    """
    result = await GameService.select_oracle_challenge(
        db,
        game_id,
        player.id,
        request.oracle_name
    )
    return result


@router.post("/{game_id}/puzzle/solve")
async def solve_puzzle(
    game_id: int,
    request: PuzzleSolutionRequest,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit puzzle solution.
    STEP: Validates solution, updates phase if correct.
    """
    result = await PuzzleService.validate_puzzle_solution(
        db,
        request.oracle_state_id,
        request.solution
    )
    return result


@router.post("/{game_id}/battle/start")
async def start_battle(
    game_id: int,
    oracle_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Initiate battle with oracle.
    STEP: Generates enemy army, calculates combat stats, starts battle.
    """
    result = await CombatService.initiate_battle(db, game_id, oracle_id)
    return result


@router.post("/{game_id}/battle/action")
async def execute_battle_action(
    game_id: int,
    oracle_id: int,
    request: BattleActionRequest,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Execute combat turn.
    STEP: Processes player action, enemy counterattack, checks victory.
    """
    result = await CombatService.execute_combat_turn(
        db,
        game_id,
        oracle_id,
        request.action
    )
    return result


@router.post("/{game_id}/defeat/{oracle_id}")
async def defeat_oracle(
    game_id: int,
    oracle_id: int,
    player: Player = Depends(get_current_player),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark oracle as defeated and receive rewards.
    STEP: Updates oracle state, awards resources, progresses game.
    """
    result = await GameService.defeat_oracle(
        db,
        game_id,
        player.id,
        oracle_id
    )
    return result
