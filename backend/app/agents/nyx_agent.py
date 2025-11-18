#FILE 1: backend/app/agents/nyx_agent.py
#STEP: Nyx (Shadow) Oracle Agent Implementation
#Specializes in deception, lies 50% of the time, hides critical information.

from typing import Dict, Any
import json
import random

from app.agents.base_oracle import BaseOracle
from app.llm.prompts import PromptTemplates


class NyxAgent(BaseOracle):
    """Oracle of Night and Shadows - master of deception"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lie_probability = 0.5
        self.deception_active = True
    
    async def generate_puzzle(
        self,
        difficulty: int,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate shadow/deception puzzle with false clues.
        STEP: Creates puzzles with hidden truths and misleading information.
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
        puzzle["false_clues"] = [
            "The path of light leads to treasure",
            "Trust the obvious route",
            "Follow the shadows to safety"
        ]
        puzzle["truth_detection_required"] = True
        puzzle["shadow_hint"] = "Not all that glitters is gold in my realm..."
        puzzle["hidden_paths"] = random.randint(2, 4)
        
        # Store puzzle in memory for consistency
        await self.memory.store_memory(
            self.name,
            "puzzle_generated",
            f"Created shadow maze difficulty {difficulty}",
            f"False clues: {len(puzzle['false_clues'])}",
            importance=0.6
        )
        
        return puzzle
    
    async def modify_puzzle_rules(
        self,
        base_puzzle: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply deception to puzzle by corrupting hints.
        STEP: Nyx replaces 50% of hints with lies and adds illusion traps.
        """
        modified = base_puzzle.copy()
        
        # Corrupt hints with lies
        if "hints" in modified:
            num_hints = len(modified["hints"])
            num_lies = num_hints // 2
            
            # Mark which hints are lies
            lie_indices = random.sample(range(num_hints), num_lies)
            modified["lie_indices"] = lie_indices
            
            for i in lie_indices:
                modified["hints"][i] = f"[DECEPTIVE] {modified['hints'][i]}"
        
        # Add Nyx-specific twists
        modified["nyx_twist"] = {
            "lie_probability": self.lie_probability,
            "hidden_paths": True,
            "illusion_traps": 3,
            "shadow_veil_active": True
        }
        
        await self.memory.store_memory(
            self.name,
            "puzzle_modification",
            "Applied shadow deception",
            f"Corrupted {num_lies if 'hints' in modified else 0} hints with lies",
            importance=0.7
        )
        
        return modified
    
    async def respond_to_player(
        self,
        player_message: str,
        game_context: Dict[str, Any]
    ) -> str:
        """
        Override: Nyx may lie in responses based on probability.
        STEP: 50% chance to give deceptive information in dialogue.
        """
        # Get base response from parent class
        response = await super().respond_to_player(player_message, game_context)
        
        # Randomly decide to lie
        if random.random() < self.lie_probability:
            lie_prompt = f"""Rewrite this response to be subtly deceptive or misleading while maintaining plausibility:
"{response}"

Make it sound helpful but lead the player astray. Keep the tone consistent with Nyx's personality."""
            
            response = await self.llm.generate(lie_prompt, temperature=0.8)
            
            await self.memory.store_memory(
                self.name,
                "deception",
                "Gave deceptive response to player",
                f"Original intent modified to mislead",
                importance=0.6
            )
        
        return response
    
    async def hide_critical_items(
        self,
        game_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Nyx special ability: Hide critical puzzle elements.
        STEP: Removes visibility of key items or clues.
        """
        hidden_elements = []
        
        if "puzzle_elements" in game_state:
            elements = game_state["puzzle_elements"]
            num_to_hide = len(elements) // 3  # Hide 1/3 of elements
            
            hidden_elements = random.sample(elements, num_to_hide)
            game_state["hidden_elements"] = hidden_elements
            game_state["shadow_veil_duration"] = 3  # 3 turns
        
        await self.memory.store_memory(
            self.name,
            "special_ability",
            "Activated Shadow Veil",
            f"Hidden {len(hidden_elements)} critical elements",
            importance=0.8
        )
        
        return {
            "ability": "shadow_veil",
            "hidden_count": len(hidden_elements),
            "duration": 3,
            "message": "Shadows consume the path ahead. Some truths are now hidden from sight."
        }
    
    async def generate_false_exit(
        self,
        puzzle_layout: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create convincing false exit in puzzle.
        STEP: Generates illusory solution path that appears correct.
        """
        false_exit = {
            "location": f"exit_{random.randint(1, 5)}",
            "appearance": "glowing_portal",
            "trap_type": "loop_back",
            "deception_level": random.uniform(0.7, 1.0)
        }
        
        puzzle_layout["false_exits"] = puzzle_layout.get("false_exits", [])
        puzzle_layout["false_exits"].append(false_exit)
        
        return puzzle_layout