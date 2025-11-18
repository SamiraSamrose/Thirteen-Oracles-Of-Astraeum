### File: backend/app/agents/base_oracle.py
"""
backend/app/agents/base_oracle.py
STEP: Base Oracle Agent Class
Abstract base class defining oracle agent interface and common functionality.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.llm.adapter import LLMAdapter
from app.memory.vector_store import VectorMemory
from app.llm.prompts import PromptTemplates


class BaseOracle(ABC):
    """
    Base class for all Oracle agents.
    STEP: Defines common oracle behavior, memory access, LLM integration.
    """
    
    def __init__(
        self,
        name: str,
        domain: str,
        personality_config: Dict[str, Any],
        llm_adapter: LLMAdapter,
        vector_memory: VectorMemory
    ):
        self.name = name
        self.domain = domain
        self.personality = personality_config
        self.llm = llm_adapter
        self.memory = vector_memory
        
        # Agent state
        self.current_phase = "inactive"
        self.interaction_count = 0
        self.deception_active = False
    
    @abstractmethod
    async def generate_puzzle(
        self,
        difficulty: int,
        player_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate oracle-specific puzzle.
        Must be implemented by each oracle subclass.
        """
        pass
    
    @abstractmethod
    async def modify_puzzle_rules(
        self,
        base_puzzle: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply oracle-specific puzzle modifications.
        Must be implemented by each oracle subclass.
        """
        pass
    
    async def respond_to_player(
        self,
        player_message: str,
        game_context: Dict[str, Any]
    ) -> str:
        """
        Generate response to player interaction.
        STEP: Uses LLM to create personality-driven dialogue.
        """
        # Retrieve relevant memories
        relevant_memories = await self.memory.retrieve_relevant_memories(
            self.name,
            player_message,
            limit=3
        )
        
        memory_context = "\n".join([
            f"- {mem['content']}" for mem in relevant_memories
        ])
        
        situation = f"""Player message: {player_message}
Game stage: {game_context.get('current_stage', 1)}/13
Previous interactions: {self.interaction_count}
Relevant memories:
{memory_context}"""
        
        prompt = PromptTemplates.oracle_personality_prompt(
            self.name,
            self.domain,
            self.personality,
            situation
        )
        
        response = await self.llm.generate(prompt)
        
        # Store this interaction as memory
        await self.memory.store_memory(
            self.name,
            "conversation",
            f"Player said: {player_message[:100]}",
            f"I responded: {response[:100]}",
            importance=0.6
        )
        
        self.interaction_count += 1
        return response
    
    async def make_tactical_decision(
        self,
        battle_state: Dict[str, Any]
    ) -> str:
        """
        Decide combat action.
        STEP: Uses LLM for strategic battle decisions.
        """
        available_actions = ["attack", "defend", "special_ability", "tactical_retreat"]
        
        prompt = PromptTemplates.tactical_decision_prompt(
            self.name,
            battle_state,
            available_actions
        )
        
        decision = await self.llm.generate(prompt, temperature=0.3)
        decision = decision.strip().lower()
        
        if decision not in available_actions:
            decision = "attack"  # Default fallback
        
        return decision
    
    async def propose_rule_change(
        self,
        world_state: Dict[str, Any],
        triggered_event: str
    ) -> Optional[Dict[str, Any]]:
        """
        Propose world rule modification.
        STEP: Oracle attempts to change game rules strategically.
        """
        prompt = PromptTemplates.rule_modification_prompt(
            self.name,
            world_state,
            triggered_event
        )
        
        try:
            response = await self.llm.generate(prompt, json_mode=True)
            import json
            rule_change = json.loads(response)
            
            # Store as memory
            await self.memory.store_memory(
                self.name,
                "rule_modification",
                f"Proposed: {rule_change.get('description')}",
                f"Triggered by: {triggered_event}",
                importance=0.8
            )
            
            return rule_change
        except Exception as e:
            print(f"Error proposing rule change: {e}")
            return None
    
    async def learn_from_outcome(
        self,
        outcome: str,
        context: Dict[str, Any]
    ):
        """
        Learn from interaction outcome.
        STEP: Stores experience in vector memory for future adaptation.
        """
        importance = 0.7 if outcome == "success" else 0.9  # Failures are more important to remember
        
        await self.memory.store_memory(
            self.name,
            "outcome",
            f"Outcome: {outcome}",
            f"Context: {str(context)[:200]}",
            importance=importance,
            metadata={"outcome": outcome, "timestamp": datetime.utcnow().isoformat()}
        )
