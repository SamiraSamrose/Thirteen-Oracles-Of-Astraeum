### File: backend/app/utils/helpers.py

"""
backend/app/utils/helpers.py
STEP: Helper Utility Functions
Common utility functions used across application.
"""
from datetime import datetime, timedelta
from typing import Any, Dict
import hashlib

def generate_game_id() -> str:
    """Generate unique game session ID"""
    timestamp = datetime.utcnow().isoformat()
    return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

def calculate_difficulty_multiplier(stage: int) -> float:
    """Calculate difficulty multiplier based on stage"""
    return 1.0 + (stage * 0.15)

def format_battle_log(action: str, damage: int, attacker: str) -> str:
    """Format battle log entry"""
    return f"{attacker} uses {action} and deals {damage} damage"

def is_game_completed(oracles_defeated: int) -> bool:
    """Check if game is completed"""
    return oracles_defeated >= 13

def calculate_reward_multiplier(difficulty: str) -> float:
    """Calculate reward multiplier based on difficulty"""
    multipliers = {"easy": 0.8, "normal": 1.0, "hard": 1.5}
    return multipliers.get(difficulty, 1.0)