### File: backend/app/agents/orchestrator.py

"""
backend/app/agents/orchestrator.py
STEP: Agent Orchestrator using LangGraph
Coordinates all 13 oracle agents, manages events, handles multi-agent interactions.
"""
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from app.llm.adapter import LLMAdapter
from app.memory.vector_store import VectorMemory
from app.agents.chronos_agent import ChronosAgent
from app.agents.nyx_agent import NyxAgent
from app.agents.athenaia_agent import AthenaiaAgent
# Import other agents...


class AgentOrchestrator:
    """
    Central coordinator for all oracle agents.
    STEP: Manages agent lifecycle, routes events, coordinates multi-agent interactions.
    """
    
    def __init__(self, llm_adapter: LLMAdapter, vector_memory: VectorMemory):
        self.llm = llm_adapter
        self.memory = vector_memory
        self.agents: Dict[str, Any] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """
        Initialize all 13 oracle agents.
        STEP: Creates agent instances with personalities and configurations.
        """
        # Agent configurations
        agent_configs = {
            "Chronos": {
                "domain": "Time and Fate",
                "personality": {
                    "cunning": 8,
                    "deception": 6,
                    "honor": 5,
                    "wisdom": 9
                },
                "class": ChronosAgent
            },
            "Nyx": {
                "domain": "Night and Shadows",
                "personality": {
                    "cunning": 9,
                    "deception": 10,
                    "honor": 3,
                    "wisdom": 7
                },
                "class": NyxAgent
            },
            "Athenaia": {
                "domain": "Wisdom and Strategy",
                "personality": {
                    "cunning": 7,
                    "deception": 4,
                    "honor": 9,
                    "wisdom": 10
                },
                "class": AthenaiaAgent
            },
            # Add other agents with BaseOracle as default
        }
        
        for name, config in agent_configs.items():
            agent_class = config.get("class", BaseOracle)
            self.agents[name] = agent_class(
                name=name,
                domain=config["domain"],
                personality_config=config["personality"],
                llm_adapter=self.llm,
                vector_memory=self.memory
            )
    
    async def route_event(
        self,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Route game event to appropriate agent(s).
        STEP: Determines which agents should respond to event.
        """
        if event_type == "oracle_challenge":
            oracle_name = event_data.get("oracle_name")
            agent = self.agents.get(oracle_name)
            
            if agent:
                response = await self._handle_oracle_challenge(agent, event_data)
                return response
        
        elif event_type == "player_action":
            # Notify all active agents
            responses = await self._broadcast_to_active_agents(event_data)
            return {"responses": responses}
        
        elif event_type == "oracle_defeated":
            # Trigger reactions from remaining agents
            reactions = await self._handle_oracle_defeat(event_data)
            return {"reactions": reactions}
        
        return {"status": "event_processed"}
    
    async def _handle_oracle_challenge(
        self,
        agent: Any,
        challenge_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle player challenging an oracle.
        STEP: Initiates puzzle generation, sets up battle, manages phases.
        """
        phase = challenge_data.get("phase", "exploration")
        
        if phase == "puzzle":
            puzzle = await agent.generate_puzzle(
                challenge_data.get("difficulty", 5),
                challenge_data.get("player_context", {})
            )
            return {"type": "puzzle", "data": puzzle}
        
        elif phase == "diplomacy":
            player_message = challenge_data.get("message", "")
            response = await agent.respond_to_player(
                player_message,
                challenge_data.get("game_context", {})
            )
            return {"type": "dialogue", "response": response}
        
        elif phase == "battle":
            decision = await agent.make_tactical_decision(
                challenge_data.get("battle_state", {})
            )
            return {"type": "tactical_decision", "action": decision}
        
        return {"type": "unknown_phase"}
    
    async def _broadcast_to_active_agents(
        self,
        event_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Broadcast event to all non-defeated agents.
        STEP: Allows agents to react to player actions collectively.
        """
        defeated_oracles = event_data.get("defeated_oracles", [])
        responses = []
        
        for name, agent in self.agents.items():
            if name not in defeated_oracles:
                # Check if agent wants to react
                should_react = await self._agent_should_react(agent, event_data)
                
                if should_react:
                    reaction = await agent.propose_rule_change(
                        event_data.get("world_state", {}),
                        event_data.get("event_type", "player_action")
                    )
                    
                    if reaction:
                        responses.append({
                            "oracle": name,
                            "reaction": reaction
                        })
        
        return responses
    
    async def _agent_should_react(
        self,
        agent: Any,
        event_data: Dict[str, Any]
    ) -> bool:
        """
        Determine if agent should react to event.
        STEP: Uses agent personality and LLM to decide reaction necessity.
        """
        # High cunning agents react more often
        cunning = agent.personality.get("cunning", 5)
        base_probability = cunning / 10.0
        
        import random
        return random.random() < base_probability
    
    async def _handle_oracle_defeat(
        self,
        defeat_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Handle aftermath of oracle defeat.
        STEP: Remaining agents adjust strategies and hostilities.
        """
        defeated_oracle = defeat_data.get("oracle_name")
        reactions = []
        
        for name, agent in self.agents.items():
            if name != defeated_oracle:
                # Allied oracles become hostile
                # Enemy oracles may become cautious
                
                reaction_prompt = f"""Oracle {name} learns that {defeated_oracle} has been defeated by the player.

How does {name} react? Consider:
- Your relationship with {defeated_oracle}
- Your own survival
- Strategic advantage

Return JSON:
{{
    "stance_change": "more_hostile|cautious|neutral",
    "strategy_adjustment": "description",
    "message_to_player": "optional taunt or warning"
}}"""
                
                try:
                    reaction_json = await self.llm.generate(reaction_prompt, json_mode=True)
                    import json
                    reaction = json.loads(reaction_json)
                    reactions.append({
                        "oracle": name,
                        "reaction": reaction
                    })
                    
                    # Store as memory
                    await agent.learn_from_outcome(
                        "ally_defeated",
                        {"defeated": defeated_oracle}
                    )
                except:
                    pass
        
        return reactions
    
    async def get_insight_hint(
        self,
        player_question: str,
        game_context: Dict[str, Any]
    ) -> str:
        """
        Generate helpful hint using knowledge oracle.
        STEP: Uses LLM to provide contextual guidance without spoiling.
        """
        from app.llm.prompts import PromptTemplates
        
        prompt = PromptTemplates.insight_hint_prompt(
            player_question,
            game_context,
            game_context.get("current_challenge", "Unknown")
        )
        
        hint = await self.llm.generate(prompt)
        return hint
    
    async def shutdown(self):
        """Clean shutdown of all agents"""
        await self.llm.close()
