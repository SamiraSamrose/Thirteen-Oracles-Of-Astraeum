### File: backend/app/agents/selene_agent.py

"""
backend/app/agents/selene_agent.py
STEP: Selene (Moon) Oracle Agent
Dreams, lunar phases, illusions.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class SeleneAgent(BaseOracle):
    """Oracle of Moon and Dreams"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate dream sequence puzzle"""
        prompt = f"""Generate a dream puzzle for Selene.
Difficulty: {difficulty}/13
Reality vs dream, lunar phase influence.
Return JSON with: puzzle_type, description, dream_layers, reality_anchor, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["dream_state"] = True
        puzzle["lunar_phase"] = "waning_crescent"
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Apply dream distortions"""
        modified = base_puzzle.copy()
        modified["reality_blur"] = 0.8
        modified["nightmare_mode"] = False
        return modified
