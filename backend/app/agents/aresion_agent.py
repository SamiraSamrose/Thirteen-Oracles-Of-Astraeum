### File: backend/app/agents/aresion_agent.py

"""
backend/app/agents/aresion_agent.py
STEP: Aresion (War) Oracle Agent
Specializes in combat, aggression, military strategy.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class AresionAgent(BaseOracle):
    """Oracle of War and Conflict"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate combat-focused puzzle"""
        prompt = f"""Generate a tactical combat puzzle for Aresion.
Difficulty: {difficulty}/13
Create a military strategy challenge with troop positioning.
Return JSON with: puzzle_type, battlefield_layout, enemy_positions, victory_conditions, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["combat_focus"] = True
        puzzle["aggression_bonus"] = difficulty * 10
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Increase combat difficulty"""
        modified = base_puzzle.copy()
        modified["enemy_reinforcements"] = True
        modified["battle_frenzy"] = {"attack_multiplier": 1.5, "defense_penalty": 0.8}
        return modified
    
    async def boost_allied_oracles(self, defeated_oracle: str) -> Dict[str, Any]:
        """Aresion boosts remaining oracle armies after defeats"""
        return {"effect": "army_boost", "multiplier": 1.2, "target": "all_hostile_oracles"}
