### File: backend/app/agents/typhon_agent.py

"""
backend/app/agents/typhon_agent.py
STEP: Typhon (Chaos) Oracle Agent - Final Boss
Combines all mechanics, rewrites rules dynamically.
"""
from typing import Dict, Any
import json
import random
from app.agents.base_oracle import BaseOracle

class TyphonAgent(BaseOracle):
    """Oracle of Chaos - The Final Trial"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.phase = 1
        self.rule_changes_applied = []
    
    async def generate_puzzle(self, difficulty: int, player_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chaotic multi-phase puzzle"""
        prompt = f"""Generate ultimate chaos puzzle for Typhon.
Phase: {self.phase}/3
Combine time, shadow, illusion, war mechanics.
Return JSON with: puzzle_type, description, chaos_elements, phase_transitions, solution"""
        
        puzzle_json = await self.llm.generate(prompt, json_mode=True)
        puzzle = json.loads(puzzle_json)
        puzzle["chaos_level"] = 10
        puzzle["combines_all_oracles"] = True
        puzzle["current_phase"] = self.phase
        return puzzle
    
    async def modify_puzzle_rules(self, base_puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically rewrite rules"""
        modified = base_puzzle.copy()
        
        # Random rule modifications
        chaos_effects = [
            {"time_reversal": True},
            {"shadow_lies": True},
            {"reality_shift": True},
            {"rule_inversion": True}
        ]
        
        selected_chaos = random.sample(chaos_effects, k=2)
        for effect in selected_chaos:
            modified.update(effect)
            self.rule_changes_applied.append(effect)
        
        await self.memory.store_memory(self.name, "chaos_applied", f"Applied: {selected_chaos}", "Entropy increases", importance=1.0)
        return modified
    
    async def advance_phase(self):
        """Move to next phase of final battle"""
        self.phase = min(3, self.phase + 1)
        return {"new_phase": self.phase, "message": f"Typhon enters phase {self.phase}!"}