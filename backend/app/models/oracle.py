### File: backend/app/models/oracle.py

"""
backend/app/models/oracle.py
STEP: Oracle Agent Models
Defines Oracle metadata, state tracking, and interaction history.
"""
from sqlalchemy import Column, Integer, String, Boolean, JSON, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Oracle(Base):
    """Oracle agent definition and metadata"""
    __tablename__ = "oracles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # e.g., "Chronos", "Nyx"
    domain = Column(String(100), nullable=False)  # e.g., "Time", "Shadow"
    
    # Description
    title = Column(String(200))  # e.g., "Oracle of Time and Fate"
    description = Column(Text)
    lore = Column(Text)
    
    # Agent configuration
    personality_config = Column(JSON)  # Loaded from YAML
    behavior_tree = Column(JSON)
    
    # Game mechanics
    difficulty_level = Column(Integer, default=1)  # 1-13
    unlock_order = Column(Integer)  # Suggested order
    
    # Rewards
    army_unit_reward = Column(String(100))  # e.g., "Frost Hoplites"
    weapon_reward = Column(String(100))  # e.g., "Temporal Dagger"
    special_ability = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    states = relationship("OracleState", back_populates="oracle")


class OracleState(Base):
    """Per-game Oracle state tracking"""
    __tablename__ = "oracle_states"
    
    id = Column(Integer, primary_key=True, index=True)
    game_state_id = Column(Integer, ForeignKey("game_states.id", ondelete="CASCADE"))
    oracle_id = Column(Integer, ForeignKey("oracles.id", ondelete="CASCADE"))
    
    # Status
    is_defeated = Column(Boolean, default=False)
    is_hostile = Column(Boolean, default=True)
    is_allied = Column(Boolean, default=False)
    
    # Interaction history
    interactions_count = Column(Integer, default=0)
    last_interaction = Column(DateTime(timezone=True))
    
    # Dynamic state
    current_phase = Column(String(50))  # exploration, puzzle, battle, confrontation
    puzzle_state = Column(JSON)
    battle_state = Column(JSON)
    diplomatic_stance = Column(Float, default=0.0)  # -1.0 to 1.0
    
    # AI behavior tracking
    deception_activated = Column(Boolean, default=False)
    special_rules_active = Column(JSON)  # Oracle-specific rule changes
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    defeated_at = Column(DateTime(timezone=True))
    
    # Relationships
    oracle = relationship("Oracle", back_populates="states")
    game_state = relationship("GameState", back_populates="oracle_states")
