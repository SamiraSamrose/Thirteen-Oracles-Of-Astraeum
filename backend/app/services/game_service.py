## STEP 4: GAME SERVICE LOGIC

### File: backend/app/services/game_service.py

"""
backend/app/services/game_service.py
STEP: Core Game Service
Manages game state, progression, inventory, and player actions.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from datetime import datetime

from app.models.player import Player
from app.models.game_state import GameState, DominionState
from app.models.oracle import Oracle, OracleState
from app.models.army import PlayerArmy, ArmyUnit


class GameService:
    """Core game logic and state management"""
    
    @staticmethod
    async def create_new_game(
        db: AsyncSession,
        player_id: int,
        difficulty: str = "normal"
    ) -> GameState:
        """
        Initialize a new game session with starting resources.
        STEP: Creates game state, initializes 13 dominions, sets up starting inventory.
        """
        # Create game state
        game_state = GameState(
            player_id=player_id,
            current_stage=1,
            oracles_defeated=0,
            gold=100,
            insight_tokens=1,
            healing_draughts=1,
            weapons=["Mortal Spear"],
            special_items=[],
            potions=["Basic Healing Draught"],
            difficulty_level=difficulty,
            world_state={
                "global_modifiers": [],
                "alliances": [],
                "hostilities": [],
                "rule_changes": []
            },
            active_events=[]
        )
        
        db.add(game_state)
        await db.flush()
        
        # Initialize all 13 oracles
        result = await db.execute(select(Oracle))
        oracles = result.scalars().all()
        
        for oracle in oracles:
            oracle_state = OracleState(
                game_state_id=game_state.id,
                oracle_id=oracle.id,
                is_defeated=False,
                is_hostile=True,
                is_allied=False,
                current_phase="locked",
                puzzle_state={},
                battle_state={},
                diplomatic_stance=-0.5,
                special_rules_active={}
            )
            db.add(oracle_state)
        
        # Initialize 13 dominions
        dominion_names = [
            ("Chronos Domain", "Chronos"),
            ("Shadow Realm of Nyx", "Nyx"),
            ("Proteus Mirage", "Proteus"),
            ("Aresion War Citadel", "Aresion"),
            ("Athenaia's Acropolis", "Athenaia"),
            ("Helios Solar Spire", "Helios"),
            ("Boreas Frozen Wastes", "Boreas"),
            ("Gaia's Living Gardens", "Gaia"),
            ("Themis Hall of Balance", "Themis"),
            ("Echo's Resonance Chamber", "Echo"),
            ("Selene's Lunar Palace", "Selene"),
            ("DelphiX Oracle Tower", "DelphiX"),
            ("Typhon's Chaos Abyss", "Typhon")
        ]
        
        for dominion_name, oracle_name in dominion_names:
            dominion = DominionState(
                game_state_id=game_state.id,
                name=dominion_name,
                oracle_name=oracle_name,
                is_controlled=False,
                is_accessible=True if oracle_name == "Chronos" else False,
                resource_bonus={},
                explored_areas=[],
                hidden_secrets=[]
            )
            db.add(dominion)
        
        # Add starting army unit
        result = await db.execute(
            select(ArmyUnit).where(ArmyUnit.name == "Novice Soldiers")
        )
        novice_unit = result.scalar_one_or_none()
        
        if novice_unit:
            player_army = PlayerArmy(
                game_state_id=game_state.id,
                army_unit_id=novice_unit.id,
                quantity=10,
                total_health=1000,
                morale=1.0,
                experience_level=1,
                is_deployed=True,
                current_location="Chronos Domain"
            )
            db.add(player_army)
        
        await db.commit()
        await db.refresh(game_state)
        
        return game_state
    
    @staticmethod
    async def get_game_state(
        db: AsyncSession,
        game_id: int,
        player_id: int
    ) -> GameState:
        """
        Get complete game state with all relationships loaded.
        STEP: Fetches game state, validates ownership, loads oracles and dominions.
        """
        result = await db.execute(
            select(GameState)
            .options(
                selectinload(GameState.oracle_states).selectinload(OracleState.oracle),
                selectinload(GameState.dominion_states),
                selectinload(GameState.player_armies).selectinload(PlayerArmy.unit_type)
            )
            .where(GameState.id == game_id, GameState.player_id == player_id)
        )
        
        game_state = result.scalar_one_or_none()
        
        if not game_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        return game_state
    
    @staticmethod
    async def save_game_state(
        db: AsyncSession,
        game_id: int,
        player_id: int
    ) -> Dict[str, Any]:
        """
        Save current game progress.
        STEP: Updates last_save timestamp and persists all changes.
        """
        game_state = await GameService.get_game_state(db, game_id, player_id)
        game_state.last_save = datetime.utcnow()
        await db.commit()
        
        return {
            "message": "Game saved successfully",
            "saved_at": game_state.last_save
        }
    
    @staticmethod
    async def select_oracle_challenge(
        db: AsyncSession,
        game_id: int,
        player_id: int,
        oracle_name: str
    ) -> Dict[str, Any]:
        """
        Select an oracle to challenge.
        STEP: Validates selection, updates game state, triggers agent initialization.
        """
        game_state = await GameService.get_game_state(db, game_id, player_id)
        
        # Find oracle
        result = await db.execute(
            select(Oracle).where(Oracle.name == oracle_name)
        )
        oracle = result.scalar_one_or_none()
        
        if not oracle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oracle not found"
            )
        
        # Get oracle state
        result = await db.execute(
            select(OracleState).where(
                OracleState.game_state_id == game_id,
                OracleState.oracle_id == oracle.id
            )
        )
        oracle_state = result.scalar_one_or_none()
        
        if oracle_state.is_defeated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Oracle already defeated"
            )
        
        # Update game state
        game_state.current_oracle_id = oracle.id
        oracle_state.current_phase = "exploration"
        oracle_state.last_interaction = datetime.utcnow()
        oracle_state.interactions_count += 1
        
        await db.commit()
        
        return {
            "oracle": {
                "name": oracle.name,
                "domain": oracle.domain,
                "title": oracle.title,
                "description": oracle.description,
                "difficulty_level": oracle.difficulty_level
            },
            "phase": "exploration",
            "message": f"You have entered the domain of {oracle.title}"
        }
    
    @staticmethod
    async def defeat_oracle(
        db: AsyncSession,
        game_id: int,
        player_id: int,
        oracle_id: int
    ) -> Dict[str, Any]:
        """
        Mark oracle as defeated and distribute rewards.
        STEP: Updates oracle state, adds rewards, increments stage, updates player stats.
        """
        game_state = await GameService.get_game_state(db, game_id, player_id)
        
        # Get oracle and state
        result = await db.execute(
            select(Oracle).where(Oracle.id == oracle_id)
        )
        oracle = result.scalar_one_or_none()
        
        result = await db.execute(
            select(OracleState).where(
                OracleState.game_state_id == game_id,
                OracleState.oracle_id == oracle_id
            )
        )
        oracle_state = result.scalar_one_or_none()
        
        if not oracle or not oracle_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oracle not found"
            )
        
        if oracle_state.is_defeated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Oracle already defeated"
            )
        
        # Mark as defeated
        oracle_state.is_defeated = True
        oracle_state.defeated_at = datetime.utcnow()
        oracle_state.is_hostile = False
        
        # Update dominion
        result = await db.execute(
            select(DominionState).where(
                DominionState.game_state_id == game_id,
                DominionState.oracle_name == oracle.name
            )
        )
        dominion = result.scalar_one_or_none()
        if dominion:
            dominion.is_controlled = True
            dominion.conquered_at = datetime.utcnow()
        
        # Award rewards
        rewards = {
            "army_unit": oracle.army_unit_reward,
            "weapon": oracle.weapon_reward,
            "special_ability": oracle.special_ability,
            "insight_tokens": 2,
            "gold": 500
        }
        
        # Add weapon to inventory
        if oracle.weapon_reward and oracle.weapon_reward not in game_state.weapons:
            game_state.weapons.append(oracle.weapon_reward)
        
        # Add insight tokens and gold
        game_state.insight_tokens += 2
        game_state.gold += 500
        
        # Add army unit
        if oracle.army_unit_reward:
            result = await db.execute(
                select(ArmyUnit).where(ArmyUnit.name == oracle.army_unit_reward)
            )
            army_unit = result.scalar_one_or_none()
            
            if army_unit:
                player_army = PlayerArmy(
                    game_state_id=game_state.id,
                    army_unit_id=army_unit.id,
                    quantity=5,
                    total_health=army_unit.health * 5,
                    morale=1.0,
                    experience_level=1,
                    is_deployed=False
                )
                db.add(player_army)
        
        # Update game progress
        game_state.oracles_defeated += 1
        game_state.current_stage = game_state.oracles_defeated + 1
        
        # Update player stats
        result = await db.execute(
            select(Player).where(Player.id == player_id)
        )
        player = result.scalar_one_or_none()
        if player:
            player.oracles_defeated += 1
        
        # Check if game is completed (all 13 oracles defeated)
        if game_state.oracles_defeated >= 13:
            game_state.is_completed = True
            game_state.completed_at = datetime.utcnow()
            if player:
                player.games_won += 1
        
        await db.commit()
        
        return {
            "message": f"Oracle {oracle.name} has been defeated!",
            "rewards": rewards,
            "progress": {
                "oracles_defeated": game_state.oracles_defeated,
                "current_stage": game_state.current_stage,
                "game_completed": game_state.is_completed
            }
        }
    
    @staticmethod
    async def use_insight_token(
        db: AsyncSession,
        game_id: int,
        player_id: int,
        question: str
    ) -> Dict[str, Any]:
        """
        Use an insight token to ask for hint/guidance.
        STEP: Validates token availability, decrements count, triggers LLM hint generation.
        """
        game_state = await GameService.get_game_state(db, game_id, player_id)
        
        if game_state.insight_tokens <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No insight tokens available"
            )
        
        game_state.insight_tokens -= 1
        await db.commit()
        
        # Return placeholder - actual LLM call handled by agent orchestrator
        return {
            "tokens_remaining": game_state.insight_tokens,
            "question": question,
            "answer_pending": True,
            "message": "Processing insight request..."
        }
    
    @staticmethod
    async def get_player_inventory(
        db: AsyncSession,
        game_id: int,
        player_id: int
    ) -> Dict[str, Any]:
        """
        Get player's complete inventory.
        STEP: Returns weapons, items, potions, armies, and resources.
        """
        game_state = await GameService.get_game_state(db, game_id, player_id)
        
        return {
            "weapons": game_state.weapons,
            "special_items": game_state.special_items,
            "potions": game_state.potions,
            "gold": game_state.gold,
            "insight_tokens": game_state.insight_tokens,
            "healing_draughts": game_state.healing_draughts,
            "armies": [
                {
                    "unit_name": army.unit_type.name,
                    "quantity": army.quantity,
                    "total_health": army.total_health,
                    "morale": army.morale,
                    "experience_level": army.experience_level,
                    "is_deployed": army.is_deployed
                }
                for army in game_state.player_armies
            ]
        }
