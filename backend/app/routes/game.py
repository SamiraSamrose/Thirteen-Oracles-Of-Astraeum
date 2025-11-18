### File: backend/app/routes/game.py

"""
backend/app/routes/game.py
STEP: Game Management API Routes
Handles game creation, state retrieval, saving, inventory management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app_puzzle_for_oracle(
        oracle_name: str,
        difficulty: int,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate puzzle based on oracle's domain and player progress.
        STEP: Creates puzzle template, will be enhanced by LLM agent.
        Returns puzzle structure to be filled by agent.
        """
        puzzle_templates = {
            "Chronos": {
                "type": "time_sequence",
                "description": "Solve the temporal paradox",
                "mechanics": ["sequence_ordering", "time_loops", "causality"]
            },
            "Nyx": {
                "type": "shadow_maze",
                "description": "Navigate through deceptive shadows",
                "mechanics": ["truth_vs_lies", "hidden_paths", "illusion_detection"]
            },
            "Proteus": {
                "type": "shape_shifter",
                "description": "Identify the true form",
                "mechanics": ["pattern_recognition", "transformation_rules", "metamorphosis"]
            },
            "Athenaia": {
                "type": "strategy_chess",
                "description": "Outsmart the wisdom oracle",
                "mechanics": ["tactical_thinking", "resource_optimization", "prediction"]
            }
        }
        
        template = puzzle_templates.get(oracle_name, {
            "type": "generic",
            "description": "Complete the trial",
            "mechanics": ["problem_solving"]
        })
        
        return {
            "oracle": oracle_name,
            "difficulty": difficulty,
            "template": template,
            "player_context": player_context,
            "status": "pending_generation"
        }
    
    @staticmethod
    async def validate_puzzle_solution(
        db: AsyncSession,
        oracle_state_id: int,
        player_solution: str
    ) -> Dict[str, Any]:
        """
        Validate player's puzzle solution.
        STEP: Checks solution against stored answer, updates puzzle state.
        """
        result = await db.execute(
            select(OracleState).where(OracleState.id == oracle_state_id)
        )
        oracle_state = result.scalar_one_or_none()
        
        if not oracle_state:
            return {"valid": False, "message": "Puzzle state not found"}
        
        puzzle_state = oracle_state.puzzle_state or {}
        correct_solution = puzzle_state.get("solution", "").lower().strip()
        player_solution = player_solution.lower().strip()
        
        is_correct = correct_solution == player_solution
        
        # Update attempts
        puzzle_state["attempts"] = puzzle_state.get("attempts", 0) + 1
        puzzle_state["last_attempt"] = player_solution
        
        if is_correct:
            puzzle_state["solved"] = True
            puzzle_state["solved_at"] = datetime.utcnow().isoformat()
            oracle_state.current_phase = "battle"  # Move to next phase
        
        oracle_state.puzzle_state = puzzle_state
        await db.commit()
        
        return {
            "valid": is_correct,
            "attempts": puzzle_state["attempts"],
            "message": "Correct! Moving to battle phase." if is_correct else "Incorrect solution. Try again.",
            "next_phase": "battle" if is_correct else "puzzle"
        }
    
    @staticmethod
    def apply_oracle_puzzle_modifier(
        base_puzzle: Dict[str, Any],
        oracle_name: str
    ) -> Dict[str, Any]:
        """
        Apply oracle-specific puzzle modifications.
        STEP: Each oracle modifies puzzles according to their domain.
        """
        modifiers = {
            "Chronos": lambda p: {**p, "time_limit": p.get("time_limit", 300) * 0.5},
            "Nyx": lambda p: {**p, "false_clues": True, "lie_probability": 0.3},
            "Proteus": lambda p: {**p, "dynamic_rules": True, "rule_changes": 3},
            "Helios": lambda p: {**p, "clue_burn_rate": 2, "progressive_difficulty": True},
            "Boreas": lambda p: {**p, "frozen_mechanics": True, "thaw_time": 60}
        }
        
        modifier = modifiers.get(oracle_name, lambda p: p)
        return modifier(base_puzzle)
