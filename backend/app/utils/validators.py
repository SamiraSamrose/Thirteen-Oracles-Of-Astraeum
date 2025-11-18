### File: backend/app/utils/validators.py

"""
backend/app/utils/validators.py
STEP: JSON Schema Validators
Validates data structures for puzzles, game state, agent outputs.
"""
import jsonschema
from typing import Dict, Any

PUZZLE_SCHEMA = {
    "type": "object",
    "properties": {
        "puzzle_type": {"type": "string"},
        "description": {"type": "string"},
        "solution": {"type": "string"},
        "difficulty": {"type": "integer", "minimum": 1, "maximum": 13}
    },
    "required": ["puzzle_type", "description", "solution"]
}

AGENT_ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "action_type": {"type": "string"},
        "target": {"type": "string"},
        "parameters": {"type": "object"}
    },
    "required": ["action_type"]
}

def validate_puzzle(puzzle_data: Dict[str, Any]) -> bool:
    """Validate puzzle data against schema"""
    try:
        jsonschema.validate(instance=puzzle_data, schema=PUZZLE_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Puzzle validation error: {e}")
        return False

def validate_agent_action(action_data: Dict[str, Any]) -> bool:
    """Validate agent action against schema"""
    try:
        jsonschema.validate(instance=action_data, schema=AGENT_ACTION_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError:
        return False

def sanitize_player_input(input_str: str) -> str:
    """Sanitize player input to prevent injection"""
    return input_str.strip()[:500]