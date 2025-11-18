### File: backend/app/agents/helios_agent.py

"""
backend/app/agents/helios_agent.py
STEP: Helios (Solar Fire) Oracle Agent
Burns clues, light-based mechanics.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class HeliosAgent(BaseOracle):
    """Oracle of Solar Fire"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate light-based puzzle"""
        prompt = f"""Generate a solar puzzle for Helios.
Difficulty: {difficulty}/13
Puzzle about light, reflection, burning away darkness.
Return JSON with: puzzle_type, description, light_sources, shadow_regions, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["clue_burn_rate"] = 2
        puzzle["solar_intensity"] = difficulty
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Burn clues over time"""
        modified = base_puzzle.copy()
        if "hints" in modified:
            modified["hint_decay"] = True
            modified["hints_remaining"] = len(modified["hints"]) - (len(modified["hints"]) // 3)
        return modified
