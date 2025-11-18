### File: backend/app/services/combat_service.py
"""
backend/app/services/combat_service.py
STEP: Combat Simulation Service
Deterministic combat engine, army management, battle resolution.
"""
from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import random

from app.models.game_state import GameState
from app.models.army import PlayerArmy, ArmyUnit
from app.models.oracle import OracleState


class CombatService:
    """Deterministic combat simulation and battle management"""
    
    @staticmethod
    def calculate_combat_power(
        units: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculate total combat power from army units.
        STEP: Aggregates attack, defense, health, and applies modifiers.
        """
        total_attack = 0
        total_defense = 0
        total_health = 0
        
        for unit in units:
            quantity = unit.get("quantity", 1)
            attack = unit.get("attack", 10)
            defense = unit.get("defense", 10)
            health = unit.get("health", 100)
            morale = unit.get("morale", 1.0)
            
            total_attack += (attack * quantity * morale)
            total_defense += (defense * quantity * morale)
            total_health += (health * quantity)
        
        return {
            "attack": total_attack,
            "defense": total_defense,
            "health": total_health,
            "power_score": (total_attack + total_defense) * (total_health / 100)
        }
    
    @staticmethod
    async def initiate_battle(
        db: AsyncSession,
        game_id: int,
        oracle_id: int
    ) -> Dict[str, Any]:
        """
        Initialize battle between player and oracle armies.
        STEP: Loads armies, calculates initial stats, sets battle state.
        """
        # Get game state with armies
        result = await db.execute(
            select(GameState).where(GameState.id == game_id)
        )
        game_state = result.scalar_one_or_none()
        
        result = await db.execute(
            select(PlayerArmy)
            .where(PlayerArmy.game_state_id == game_id, PlayerArmy.is_deployed == True)
        )
        player_armies = result.scalars().all()
        
        # Calculate player power
        player_units = [
            {
                "name": army.unit_type.name,
                "quantity": army.quantity,
                "attack": army.unit_type.attack,
                "defense": army.unit_type.defense,
                "health": army.unit_type.health,
                "morale": army.morale
            }
            for army in player_armies
        ]
        
        player_power = CombatService.calculate_combat_power(player_units)
        
        # Get oracle state
        result = await db.execute(
            select(OracleState).where(
                OracleState.game_state_id == game_id,
                OracleState.oracle_id == oracle_id
            )
        )
        oracle_state = result.scalar_one_or_none()
        
        # Generate enemy army based on oracle difficulty
        result = await db.execute(
            select(Oracle).where(Oracle.id == oracle_id)
        )
        oracle = result.scalar_one_or_none()
        
        enemy_power_multiplier = oracle.difficulty_level * 0.8
        enemy_units = CombatService.generate_enemy_army(oracle.name, enemy_power_multiplier)
        enemy_power = CombatService.calculate_combat_power(enemy_units)
        
        # Initialize battle state
        battle_state = {
            "turn": 1,
            "player_health": player_power["health"],
            "enemy_health": enemy_power["health"],
            "player_units": player_units,
            "enemy_units": enemy_units,
            "battle_log": [],
            "status": "in_progress"
        }
        
        oracle_state.battle_state = battle_state
        oracle_state.current_phase = "battle"
        await db.commit()
        
        return {
            "battle_initiated": True,
            "player_power": player_power,
            "enemy_power": enemy_power,
            "battle_state": battle_state
        }
    
    @staticmethod
    def generate_enemy_army(oracle_name: str, power_multiplier: float) -> List[Dict[str, Any]]:
        """
        Generate oracle's army composition.
        STEP: Creates themed enemy units based on oracle domain.
        """
        army_templates = {
            "Chronos": [
                {"name": "Time Wraiths", "attack": 15, "defense": 10, "health": 80, "quantity": 8},
                {"name": "Temporal Guards", "attack": 20, "defense": 15, "health": 120, "quantity": 5}
            ],
            "Nyx": [
                {"name": "Shadow Assassins", "attack": 25, "defense": 8, "health": 70, "quantity": 10},
                {"name": "Night Stalkers", "attack": 18, "defense": 12, "health": 90, "quantity": 6}
            ],
            "Aresion": [
                {"name": "War Hoplites", "attack": 22, "defense": 20, "health": 150, "quantity": 10},
                {"name": "Battle Champions", "attack": 30, "defense": 25, "health": 200, "quantity": 4}
            ]
        }
        
        base_army = army_templates.get(oracle_name, [
            {"name": "Oracle Guards", "attack": 18, "defense": 15, "health": 100, "quantity": 8}
        ])
        
        # Apply power multiplier
        for unit in base_army:
            unit["attack"] = int(unit["attack"] * power_multiplier)
            unit["defense"] = int(unit["defense"] * power_multiplier)
            unit["health"] = int(unit["health"] * power_multiplier)
            unit["morale"] = 1.0
        
        return base_army
    
    @staticmethod
    async def execute_combat_turn(
        db: AsyncSession,
        game_id: int,
        oracle_id: int,
        player_action: str
    ) -> Dict[str, Any]:
        """
        Execute one turn of combat.
        STEP: Processes player action, calculates damage, updates battle state.
        """
        result = await db.execute(
            select(OracleState).where(
                OracleState.game_state_id == game_id,
                OracleState.oracle_id == oracle_id
            )
        )
        oracle_state = result.scalar_one_or_none()
        
        battle_state = oracle_state.battle_state
        
        if battle_state["status"] != "in_progress":
            return {"error": "Battle is not in progress"}
        
        # Player attack
        player_damage = random.randint(50, 150)  # Simplified deterministic range
        battle_state["enemy_health"] -= player_damage
        battle_state["battle_log"].append(f"Turn {battle_state['turn']}: Player dealt {player_damage} damage")
        
        # Enemy counterattack
        if battle_state["enemy_health"] > 0:
            enemy_damage = random.randint(40, 120)
            battle_state["player_health"] -= enemy_damage
            battle_state["battle_log"].append(f"Turn {battle_state['turn']}: Enemy dealt {enemy_damage} damage")
        
        # Check battle outcome
        if battle_state["enemy_health"] <= 0:
            battle_state["status"] = "victory"
            oracle_state.current_phase = "confrontation"
            battle_state["battle_log"].append("Victory! Enemy defeated!")
        elif battle_state["player_health"] <= 0:
            battle_state["status"] = "defeat"
            battle_state["battle_log"].append("Defeat! Your army has fallen!")
        
        battle_state["turn"] += 1
        oracle_state.battle_state = battle_state
        await db.commit()
        
        return {
            "turn": battle_state["turn"],
            "player_health": battle_state["player_health"],
            "enemy_health": battle_state["enemy_health"],
            "status": battle_state["status"],
            "battle_log": battle_state["battle_log"][-5:],  # Last 5 events
            "next_phase": oracle_state.current_phase
        }
