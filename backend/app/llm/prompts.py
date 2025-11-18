### File: backend/app/llm/prompts.py

"""
backend/app/llm/prompts.py
STEP: Structured Prompt Templates
Defines prompts for different agent types and actions.
"""
from typing import Dict, Any


class PromptTemplates:
    """Centralized prompt templates for LLM calls"""
    
    @staticmethod
    def oracle_personality_prompt(
        oracle_name: str,
        domain: str,
        personality_traits: Dict[str, Any],
        current_situation: str
    ) -> str:
        """
        Generate oracle personality-driven response.
        STEP: Creates context-aware prompt for oracle agent behavior.
        """
        return f"""You are {oracle_name}, the Oracle of {domain}.

Personality Traits:
- Cunning Level: {personality_traits.get('cunning', 5)}/10
- Deception: {personality_traits.get('deception', 5)}/10
- Honor: {personality_traits.get('honor', 5)}/10
- Wisdom: {personality_traits.get('wisdom', 5)}/10

Current Situation:
{current_situation}

You must respond in character, considering your domain expertise and personality.
Your goal is to challenge the player while maintaining your oracle persona.

Response:"""
    
    @staticmethod
    def puzzle_generation_prompt(
        oracle_name: str,
        difficulty: int,
        puzzle_type: str,
        player_progress: Dict[str, Any]
    ) -> str:
        """
        Generate puzzle creation prompt.
        STEP: Instructs LLM to create valid puzzle in JSON format.
        """
        return f"""Generate a {puzzle_type} puzzle for {oracle_name}'s domain.

Difficulty Level: {difficulty}/13
Player Progress: {player_progress.get('oracles_defeated', 0)} oracles defeated

Requirements:
1. Puzzle must be solvable but challenging
2. Must fit the oracle's domain theme
3. Include clear description and solution
4. Provide 2-3 hints of increasing specificity

Return ONLY valid JSON with this structure:
{{
    "puzzle_type": "{puzzle_type}",
    "description": "puzzle description",
    "solution": "correct answer",
    "hints": ["hint1", "hint2", "hint3"],
    "difficulty": {difficulty}
}}"""
    
    @staticmethod
    def diplomatic_response_prompt(
        oracle_name: str,
        player_message: str,
        relationship_status: float,
        oracle_goals: List[str]
    ) -> str:
        """
        Generate diplomatic conversation.
        STEP: Creates oracle's response to player diplomacy attempts.
        """
        stance = "hostile" if relationship_status < -0.3 else "neutral" if relationship_status < 0.3 else "friendly"
        
        return f"""You are {oracle_name}. The player says: "{player_message}"

Your current stance toward the player: {stance} ({relationship_status})
Your goals: {', '.join(oracle_goals)}

Respond in character. You may:
- Negotiate terms
- Reveal information (truthfully or deceptively)
- Make demands or offers
- Challenge the player's reasoning

Keep response under 100 words. Be strategic and stay in character.

Response:"""
    
    @staticmethod
    def tactical_decision_prompt(
        oracle_name: str,
        battle_state: Dict[str, Any],
        available_actions: List[str]
    ) -> str:
        """
        Generate tactical combat decision.
        STEP: Instructs agent to choose optimal battle action.
        """
        return f"""You are {oracle_name} commanding your army in battle.

Battle State:
- Your Health: {battle_state.get('enemy_health', 0)}
- Player Health: {battle_state.get('player_health', 0)}
- Turn: {battle_state.get('turn', 1)}

Available Actions: {', '.join(available_actions)}

Choose the best tactical action based on current situation.
Return ONLY the action name, nothing else.

Action:"""
    
    @staticmethod
    def insight_hint_prompt(
        player_question: str,
        game_context: Dict[str, Any],
        current_challenge: str
    ) -> str:
        """
        Generate helpful hint/guidance.
        STEP: Creates insight response from knowledge oracle.
        """
        return f"""A player seeks guidance with this question: "{player_question}"

Current Challenge: {current_challenge}
Game Context: Oracle stage {game_context.get('current_stage', 1)}/13

Provide a helpful but not overly revealing hint. Guide them toward the solution without giving it away directly.
Keep response under 80 words.

Hint:"""
    
    @staticmethod
    def rule_modification_prompt(
        oracle_name: str,
        world_state: Dict[str, Any],
        triggered_event: str
    ) -> str:
        """
        Generate oracle's rule change request.
        STEP: Oracle proposes world rule modifications.
        """
        return f"""You are {oracle_name}. A player action has triggered: {triggered_event}

Current World State:
{json.dumps(world_state, indent=2)}

You may propose ONE rule modification to make the game more challenging or unpredictable.

Return ONLY valid JSON:
{{
    "rule_type": "combat_modifier|puzzle_twist|resource_drain|ally_betrayal",
    "description": "what changes",
    "affected_domains": ["domain1", "domain2"],
    "duration": "turns or permanent"
}}"""
