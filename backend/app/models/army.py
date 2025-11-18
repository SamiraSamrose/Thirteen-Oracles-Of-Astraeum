### File: backend/app/models/army.py

"""
backend/app/models/army.py
STEP: Army and Unit Models
Defines army units, player's military forces, and combat capabilities.
"""
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ArmyUnit(Base):
    """Army unit type definition (template)"""
    __tablename__ = "army_units"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    unit_type = Column(String(50), nullable=False)  # infantry, cavalry, archer, special
    
    # Description
    description = Column(Text)
    origin_oracle = Column(String(100))  # Which Oracle rewards this unit
    
    # Combat stats
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=10)
    health = Column(Integer, default=100)
    speed = Column(Integer, default=5)
    
    # Special abilities
    special_abilities = Column(JSON, default=list)
    element_affinity = Column(String(50))  # fire, ice, shadow, light, etc.
    
    # Cost/Rarity
    recruitment_cost = Column(Integer, default=50)
    rarity = Column(String(20), default="common")  # common, rare, legendary
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlayerArmy(Base):
    """Player's army composition in a specific game"""
    __tablename__ = "player_armies"
    
    id = Column(Integer, primary_key=True, index=True)
    game_state_id = Column(Integer, ForeignKey("game_states.id", ondelete="CASCADE"))
    army_unit_id = Column(Integer, ForeignKey("army_units.id"))
    
    # Army composition
    quantity = Column(Integer, default=1)
    total_health = Column(Integer)  # Aggregate health
    
    # Combat modifiers
    morale = Column(Float, default=1.0)  # 0.5 to 1.5
    experience_level = Column(Integer, default=1)
    
    # Status
    is_deployed = Column(Boolean, default=False)
    current_location = Column(String(100))  # Which dominion
    
    # Timestamps
    recruited_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    game_state = relationship("GameState", back_populates="player_armies")
    unit_type = relationship("ArmyUnit")
