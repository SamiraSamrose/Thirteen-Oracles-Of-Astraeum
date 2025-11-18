### File: backend/app/agents/echo_agent.py

"""
backend/app/agents/echo_agent.py
STEP: Echo (Sound) Oracle Agent
Audio puzzles, voice manipulation, resonance.
"""
from typing import Dict, Any
import json
from app.agents.base_oracle import BaseOracle

class EchoAgent(BaseOracle):
    """Oracle of Sound and Voice"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate audio puzzle"""
        prompt = f"""Generate a sound-based puzzle for Echo.
Difficulty: {difficulty}/13
Audio pattern recognition or voice manipulation.
Return JSON with: puzzle_type, description, sound_sequence, pattern_rule, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["audio_based"] = True
        puzzle["resonance_required"] = True
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Apply echo effects"""
        modified = base_puzzle.copy()
        modified["echo_distortion"] = True
        modified["reverb_level"] = 0.7
        return modified
