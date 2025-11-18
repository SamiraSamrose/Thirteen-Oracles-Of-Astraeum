### File: backend/app/services/puzzle_service.py

"""
backend/app/services/puzzle_service.py
STEP: Puzzle Generation and Validation Service
Generates puzzles using LLM, validates solutions, tracks puzzle state.
"""
from typing import Dict, Any, Optional
import json
import jsonschema
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.oracle import OracleState


class PuzzleService:
    """Puzzle generation, validation, and state management"""
    
    # Puzzle type schemas for validation
    PUZZLE_SCHEMAS = {
        "logic": {
            "type": "object",
            "properties": {
                "puzzle_type": {"type": "string"},
                "description": {"type": "string"},
                "solution": {"type": "string"},
                "hints": {"type": "array"},
                "difficulty": {"type": "integer"}
            },
            "required": ["puzzle_type", "description", "solution"]
        },
        "riddle": {
            "type": "object",
            "properties": {
                "riddle_text": {"type": "string"},
                "answer": {"type": "string"},
                "alternative_answers": {"type": "array"}
            },
            "required": ["riddle_text", "answer"]
        },
        "pattern": {
            "type": "object",
            "properties": {
                "sequence": {"type": "array"},
                "next_value": {"type": "string"},
                "pattern_rule": {"type": "string"}
            },
            "required": ["sequence", "next_value"]
        }
    }
    
    @staticmethod
    def validate_puzzle_schema(puzzle_data: Dict[str, Any], puzzle_type: str) -> bool:
        """
        Validate puzzle data against schema.
        STEP: Uses JSON schema validation to ensure puzzle integrity.
        """
        try:
            schema = PuzzleService.PUZZLE_SCHEMAS.get(puzzle_type)
            if not schema:
                return False
            
            jsonschema.validate(instance=puzzle_data, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False
    
    @staticmethod
    async def generate_puzzle(
        self,
        difficulty: int,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate shadow/deception puzzle.
        STEP: Creates puzzles with hidden truths and false clues.
        """
        prompt = PromptTemplates.puzzle_generation_prompt(
            self.name,
            difficulty,
            "shadow_maze",
            player_context
        )
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        
        # Add Nyx-specific deception mechanics
        puzzle["false_clues"] = ["Path of light leads to treasure", "Trust the obvious route"]
        puzzle["truth_detection_required"] = True
        puzzle["shadow_hint"] = "Not all that glitters is gold..."
        
        return puzzle
    
    async def modify_puzzle_rules(
        self,
        base_puzzle: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply deception to puzzle.
        STEP: Nyx adds false hints and misleading information.
        """
        modified = base_puzzle.copy()
        
        # Corrupt hints with lies
        if "hints" in modified:
            # Replace 50% of hints with lies
            num_lies = len(modified["hints"]) // 2
            for i in range(num_lies):
                modified["hints"][i] = f"[DECEPTIVE] {modified['hints'][i]}"
        
        modified["nyx_twist"] = {
            "lie_probability": self.lie_probability,
            "hidden_paths": True,
            "illusion_traps": 3
        }
        
        await self.memory.store_memory(
            self.name,
            "puzzle_modification",
            "Applied shadow deception",
            "Corrupted hints with lies",
            importance=0.7
        )
        
        return modified
    
    async def respond_to_player(
        self,
        player_message: str,
        game_context: Dict[str, Any]
    ) -> str:
        """
        Override: Nyx may lie in responses.
        STEP: 50% chance to give deceptive information.
        """
        response = await super().respond_to_player(player_message, game_context)
        
        # Randomly decide to lie
        if random.random() < self.lie_probability:
            lie_prompt = f"Rewrite this response to be subtly deceptive or misleading: {response}"
            response = await self.llm.generate(lie_prompt, temperature=0.8)
            
            await self.memory.store_memory(
                self.name,
                "deception",
                "Gave deceptive response",
                f"Original was truthful, now misleading",
                importance=0.6
            )
        
        return response
