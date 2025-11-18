### File: backend/app/agents/boreas_agent.py

"""
backend/app/agents/boreas_agent.py
STEP: Boreas (Winter Storm) Oracle Agent
Ice, freezing mechanics, slowing effects.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class BoreasAgent(BaseOracle):
    """Oracle of Winter Storms"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ice puzzle"""
        prompt = f"""Generate a winter puzzle for Boreas.
Difficulty: {difficulty}/13
Puzzle involving ice, freezing, thawing sequences.
Return JSON with: puzzle_type, description, frozen_elements, thaw_sequence, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["freeze_mechanics"] = True
        puzzle["thaw_time"] = 60
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Apply freezing effects"""
        modified = base_puzzle.copy()
        modified["frozen_progress"] = True
        modified["ice_hazards"] = {"damage": 10, "slow": 0.5}
        return modified
