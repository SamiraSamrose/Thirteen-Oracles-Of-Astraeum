### File: docs/AGENT_DESIGN.md

# Agent Design Documentation

## Overview
Each oracle is an isolated AI agent with unique personality, goals, and mechanics. Agents use LLM for dialogue/decisions and vector memory for learning.

## Agent Architecture

### Base Components
- **Personality Config**: YAML defining traits (cunning, deception, honor, wisdom)
- **Behavior Tree**: Decision logic for puzzle generation, combat, diplomacy
- **Memory**: Weaviate vector store for experiences and player patterns
- **LLM Integration**: Ollama/vLLM for natural language generation

### Agent Lifecycle
1. **Initialization**: Load personality, connect to LLM and memory
2. **Event Subscription**: Subscribe to relevant game events via Redis
3. **Decision Making**: Process events, consult memory, generate actions
4. **Output Validation**: Validate actions against schema before execution
5. **Memory Update**: Store outcomes for future learning

## Oracle-Specific Mechanics

### Chronos (Time)
- **Specialty**: Temporal manipulation
- **Mechanics**: Rewinds, time limits, causality puzzles
- **Deception**: Honest but cryptic

### Nyx (Shadow)
- **Specialty**: Deception
- **Mechanics**: 50% lie rate, hidden elements
- **Deception**: Extremely high

### Typhon (Chaos)
- **Specialty**: Rule rewriting
- **Mechanics**: Dynamic difficulty, combines all mechanics
- **Phases**: Three-stage final battle

## Multi-Agent Interactions

### Communication
- Agents communicate via## Winning Conditions

### Victory
- Defeat all 13 oracles
- Unify Astraeum under your banner
- Final confrontation with Typhon

### Defeat
- All armies eliminated
- Resources depleted
- Trapped by oracle mechanics

### Alternate Endings
- Diplomatic victory (ally with majority)
- Betrayal ending (side with chaos)
- Perfect run (no defeats, all secrets)