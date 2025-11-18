### File: backend/app/agents/athenaia_agent.py

"""
backend/app/agents/athenaia_agent.py
STEP: Athenaia (Wisdom) Oracle Agent
Specializes in strategy, chess-like puzzles, tactical complexity.
"""
from typing import Dict, Any
import json

from app.agents.base_oracle import BaseOracle
from app.llm.prompts import PromptTemplates


class AthenaiaAgent(BaseOracle):
    """Oracle of Wisdom and Strategy - master tactician"""
    
    async def generate_puzzle(
        self,
        difficulty: int,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate strategic puzzle.
        STEP: Creates chess-like tactical challenges.
        """
        prompt = f"""Generate a strategic puzzle for Athenaia, Oracle of Wisdom.

Difficulty: {difficulty}/13
Player has defeated: {player_context.get('oracles_defeated', 0)} oracles

Create a tactical positioning puzzle where the player must optimize resource placement.

Return JSON:
{{
    "puzzle_type": "strategic_positioning",
    "description": "puzzle description",
    "board_size": "grid dimensions",
    "pieces": ["list of pieces"],
    "solution": "optimal configuration",
    "hints": ["tactical hints"],
    "difficulty": {difficulty}
}}"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        
        # Add Athenaia-specific mechanics
        puzzle["strategic_depth"] = difficulty
        puzzle["counter_moves"] = True
        puzzle["wisdom_hint"] = "Strategy defeats strength..."
        
        return puzzle
    
    async def modify_puzzle_rules(
        self,
        base_puzzle: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Increase puzzle complexity.
        STEP: Athenaia adds additional constraints and strategic layers.
        """
        modified = base_puzzle.copy()
        
        # Increase complexity if player is solving too fast
        modified["athenaia_twist"] = {
            "additional_constraints": 2,
            "multi_step_solution": True,
            "counter_strategy_active": True,
            "complexity_multiplier": 1.5
        }
        
        await self.memory.store_memory(
            self.name,
            "puzzle_modification",
            "Increased strategic complexity",
            "Added constraints and multi-step requirements",
            importance=0.7
        )
        
        return modified
    
    async def analyze_player_strategy(
        self,
        player_actions: list
    ) -> Dict[str, Any]:
        """
        Analyze player's tactical patterns.
        STEP: Uses LLM to identify player strategy weaknesses.
        """
        actions_summary = ", ".join(player_actions[-10:])  # Last 10 actions
        
        prompt = f"""Analyze this player's strategic patterns:
{actions_summary}

Identify:
1. Their preferred tactics
2. Weaknesses in their approach
3. Optimal counter-strategy

Return JSON with analysis."""
        
        analysis_json = await self.llm.generate(prompt, json_mode=True)
        analysis = json.loads(analysis_json)
        
        # Store learned pattern
        await self.memory.store_memory(
            self.name,
            "player_analysis",
            f"Identified player patterns",
            str(analysis),
            importance=0.9
        )
        
        return analysis
