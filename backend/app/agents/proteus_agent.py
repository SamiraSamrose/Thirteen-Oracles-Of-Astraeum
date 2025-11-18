## REMAINING AGENT IMPLEMENTATIONS

### File: backend/app/agents/proteus_agent.py

"""
backend/app/agents/proteus_agent.py
STEP: Proteus (Illusion) Oracle Agent
Specializes in transformation, shape-shifting, dynamic rule changes.
"""
from typing import Dict, Any
import json
import random
from app.agents.base_oracle import BaseOracle

class ProteusAgent(BaseOracle):
    """Oracle of Illusion and Transformation"""
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate shape-shifting puzzle"""
        prompt = f"""Generate a transformation puzzle for Proteus.
Difficulty: {difficulty}/13
Create a pattern recognition puzzle where rules change mid-solve.
Return JSON with: puzzle_type, description, initial_rule, rule_changes, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["proteus_twist"] = {"rule_shifts": 3, "metamorphosis_active": True}
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Apply dynamic rule changes"""
        modified = base_puzzle.copy()
        modified["dynamic_rules"] = True
        modified["rule_change_triggers"] = [25, 50, 75]  # Percentage completion
        await self.memory.store_memory(self.name, "puzzle_modification", "Applied metamorphosis", "Rules shift at checkpoints", importance=0.7)
        return modified