### File: backend/app/models/game_state.py

"""
backend/app/models/game_state.py
STEP: Game State Models
Tracks overall game progress, dominion control, and world state.
"""
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class GameState(Base):
    """Main game session state"""
    __tablename__ = "game_states"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    
    # Game progress
    current_stage = Column(Integer, default=1)  # 1-13
    oracles_defeated = Column(Integer, default=0)
    current_oracle_id = Column(Integer, ForeignKey("oracles.id"))
    
    # Player resources
    gold = Column(Integer, default=100)
    insight_tokens = Column(Integer, default=1)
    healing_draughts = Column(Integer, default=1)
    
    # Inventory
    weapons = Column(JSON, default=list)  # ["Mortal Spear", ...]
    special_items = Column(JSON, default=list)
    potions = Column(JSON, default=list)
    
    # Game status
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    difficulty_level = Column(String(20), default="normal")  # easy, normal, hard
    
    # World state
    world_state = Column(JSON)  # Global rule changes, alliances, etc.
    active_events = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    last_save = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    player = relationship("Player", back_populates="game_states")
    oracle_states = relationship("OracleState", back_populates="game_state", cascade="all, delete-orphan")
    dominion_states = relationship("DominionState", back_populates="game_state", cascade="all, delete-orphan")
    player_armies = relationship("PlayerArmy", back_populates="game_state", cascade="all, delete-orphan")


class DominionState(Base):
    """State of each of the 13 floating dominions"""
    __tablename__ = "dominion_states"
    
    id = Column(Integer, primary_key=True, index=True)
    game_state_id = Column(Integer, ForeignKey("game_states.id", ondelete="CASCADE"))
    
    # Dominion info
    name = Column(String(100), nullable=False)
    oracle_name = Column(String(100), nullable=False)
    
    # Control
    is_controlled = Column(Boolean, default=False)
    is_accessible = Column(Boolean, default=True)
    
    # Resources
    resource_bonus = Column(JSON)  # Special bonuses this dominion provides
    
    # Map state
    explored_areas = Column(JSON, default=list)
    hidden_secrets = Column(JSON, default=list)
    
    # Timestamps
    conquered_at = Column(DateTime(timezone=True))
    
    # Relationship
    game_state = relationship("GameState", back_populates="dominion_states")
