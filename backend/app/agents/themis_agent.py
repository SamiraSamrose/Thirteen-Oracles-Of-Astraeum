### File: backend/app/agents/themis_agent.py

"""
backend/app/agents/themis_agent.py
STEP: Themis (Law/Justice) Oracle Agent
Judges moral choices, punishes contradictions.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class ThemisAgent(BaseOracle):
    """Oracle of Law and Balance"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate moral dilemma puzzle"""
        prompt = f"""Generate a justice puzzle for Themis.
Difficulty: {difficulty}/13
Moral dilemma with consequences for contradictory choices.
Return JSON with: puzzle_type, description, choices, consequences, just_solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["moral_tracking"] = True
        return puzzle
    
    async def judge_player_actions(self, player_history: list) -> Dict[str, Any]:
        """Analyze for moral contradictions"""
        contradictions = []
        for i, action in enumerate(player_history[:-1]):
            if self._is_contradictory(action, player_history[i+1:]):
                contradictions.append(action)
        
        if contradictions:
            return {"judgment": "guilty", "penalty": len(contradictions) * 100, "crimes": contradictions}
        return {"judgment": "innocent", "reward": 50}
    
    def _is_contradictory(self, action: str, future_actions: list) -> bool:
        """Check if action contradicts future choices"""
        return False  # Simplified logic
