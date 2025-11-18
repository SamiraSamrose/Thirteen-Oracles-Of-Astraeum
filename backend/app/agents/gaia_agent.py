### File: backend/app/agents/gaia_agent.py

"""
backend/app/agents/gaia_agent.py
STEP: Gaia (Earth) Oracle Agent
Growth, shifting terrain, living puzzles.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class GaiaAgent(BaseOracle):
    """Oracle of Earth and Growth"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate earth-based puzzle"""
        prompt = f"""Generate a living earth puzzle for Gaia.
Difficulty: {difficulty}/13
Puzzle that grows and shifts as player solves it.
Return JSON with: puzzle_type, description, growth_pattern, shift_rules, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["living_puzzle"] = True
        puzzle["growth_rate"] = difficulty * 0.1
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Make puzzle evolve"""
        modified = base_puzzle.copy()
        modified["tectonic_shift"] = True
        modified["terrain_changes"] = {"frequency": 30, "magnitude": "medium"}
        return modified
