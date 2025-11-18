### File: backend/app/agents/chronos_agent.py
"""
backend/app/agents/chronos_agent.py
STEP: Chronos (Time) Oracle Agent
Specializes in time manipulation, rewinds, temporal paradoxes.
"""
from typing import Dict, Any
import json

from app.agents.base_oracle import BaseOracle
from app.llm.prompts import PromptTemplates


class ChronosAgent(BaseOracle):
    """Oracle of Time and Fate - manipulates temporal mechanics"""
    
    async def generate_puzzle(
        self,
        difficulty: int,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate time-based puzzle.
        STEP: Creates sequence/causality puzzles with LLM assistance.
        """
        prompt = PromptTemplates.puzzle_generation_prompt(
            self.name,
            difficulty,
            "temporal_sequence",
            player_context
        )
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        
        # Add Chronos-specific mechanics
        puzzle["time_limit"] = max(60, 300 - (difficulty * 20))  # Decreasing time
        puzzle["rewind_allowed"] = difficulty < 7
        puzzle["temporal_hint"] = "Time flows differently here..."
        
        return puzzle
    
    async def modify_puzzle_rules(
        self,
        base_puzzle: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply time manipulation to puzzle.
        STEP: Chronos reduces time limits and adds rewind mechanics.
        """
        modified = base_puzzle.copy()
        
        # Reduce time limit
        if "time_limit" in modified:
            modified["time_limit"] = int(modified["time_limit"] * 0.5)
        
        # Add temporal challenges
        modified["chronos_twist"] = {
            "rewind_on_wrong_answer": True,
            "repeating_sequence": True,
            "causality_check": True
        }
        
        await self.memory.store_memory(
            self.name,
            "puzzle_modification",
            "Applied temporal restrictions",
            f"Time limit halved, rewind mechanics active",
            importance=0.7
        )
        
        return modified
    
    async def special_ability_rewind(
        self,
        game_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Chronos special: Rewind last player action.
        STEP: Cancels player's most recent reward or progress.
        """
        result = {
            "ability": "temporal_rewind",
            "message": f"{self.name} manipulates time! Your last action is undone.",
            "effect": "last_reward_cancelled"
        }
        
        await self.memory.store_memory(
            self.name,
            "special_ability",
            "Used Temporal Rewind",
            f"Cancelled player progress",
            importance=0.8
        )
        
        return result
