### File: backend/tests/test_game_logic.py

"""
backend/tests/test_game_logic.py
STEP: Game Logic Testing
Tests game state, progression, combat, rewards.
"""
import pytest
from app.services.game_service import GameService
from app.services.combat_service import CombatService

@pytest.mark.asyncio
async def test_game_creation(db_session):
    """Test game initialization"""
    game_state = await GameService.create_new_game(db_session, player_id=1)
    assert game_state.current_stage == 1
    assert game_state.insight_tokens == 1
    assert len(game_state.weapons) == 1

@pytest.mark.asyncio
async def test_combat_calculation():
    """Test combat power calculation"""
    units = [{"quantity": 10, "attack": 10, "defense": 10, "health": 100, "morale": 1.0}]
    power = CombatService.calculate_combat_power(units)
    assert power["attack"] == 100
    assert power["health"] == 1000
