### File: backend/tests/test_agents.py

"""
backend/tests/test_agents.py
STEP: Agent Testing Suite
Tests oracle agent behavior, LLM integration, memory storage.
"""
import pytest
from app.agents.chronos_agent import ChronosAgent
from app.agents.nyx_agent import NyxAgent
from app.llm.adapter import LLMAdapter
from app.memory.vector_store import VectorMemory

@pytest.mark.asyncio
async def test_chronos_puzzle_generation():
    """Test Chronos generates valid time puzzles"""
    llm = LLMAdapter()
    memory = VectorMemory()
    agent = ChronosAgent("Chronos", "Time", {}, llm, memory)
    
    puzzle = await agent.generate_puzzle(5, {"oracles_defeated": 2})
    assert "time_limit" in puzzle
    assert puzzle["time_limit"] > 0

@pytest.mark.asyncio
async def test_nyx_deception():
    """Test Nyx applies deception mechanics"""
    llm = LLMAdapter()
    memory = VectorMemory()
    agent = NyxAgent("Nyx", "Shadow", {"deception": 10}, llm, memory)
    
    puzzle = {"hints": ["hint1", "hint2", "hint3"]}
    modified = await agent.modify_puzzle_rules(puzzle)
    assert "nyx_twist" in modified
