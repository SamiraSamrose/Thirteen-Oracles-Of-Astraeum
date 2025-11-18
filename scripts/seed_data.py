### File: scripts/seed_data.py

"""
scripts/seed_data.py
STEP: Database Seeding Script
Populates database with 13 oracles, army units, initial configurations.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, init_db
from app.models.oracle import Oracle
from app.models.army import ArmyUnit


async def seed_oracles(db: AsyncSession):
    """Seed 13 oracle definitions"""
    oracles_data = [
        {
            "name": "Chronos",
            "domain": "Time and Fate",
            "title": "Oracle of Time and Fate",
            "description": "Master of temporal flows, can rewind actions and predict futures",
            "lore": "Once the keeper of Astraeum's timeline, now uses time as a weapon",
            "difficulty_level": 3,
            "unlock_order": 1,
            "army_unit_reward": "Temporal Guards",
            "weapon_reward": "Temporal Dagger",
            "special_ability": "Time Rewind",
            "personality_config": {
                "cunning": 8,
                "deception": 6,
                "honor": 5,
                "wisdom": 9
            }
        },
        {
            "name": "Nyx",
            "domain": "Night and Shadows",
            "title": "Oracle of Night and Shadows",
            "description": "Mistress of deception, lies 50% of the time",
            "lore": "Dwells in eternal darkness, truth and lies are indistinguishable",
            "difficulty_level": 4,
            "unlock_order": 2,
            "army_unit_reward": "Shadow Stalkers",
            "weapon_reward": "Shadowblade",
            "special_ability": "Shadow Veil",
            "personality_config": {
                "cunning": 9,
                "deception": 10,
                "honor": 3,
                "wisdom": 7
            }
        },
        {
            "name": "Proteus",
            "domain": "Illusion and Transformation",
            "title": "Oracle of Illusion",
            "description": "Shape-shifter who changes puzzle rules unexpectedly",
            "lore": "No one has seen his true form in centuries",
            "difficulty_level": 5,
            "unlock_order": 3,
            "army_unit_reward": "Illusionary Doppels",
            "weapon_reward": "Mirror Shield",
            "special_ability": "Reality Warp",
            "personality_config": {
                "cunning": 8,
                "deception": 9,
                "honor": 4,
                "wisdom": 6
            }
        },
        {
            "name": "Aresion",
            "domain": "War and Conflict",
            "title": "Oracle of War",
            "description": "Forces combat puzzles and boosts enemy armies",
            "lore": "Thrives on battle, every defeat makes him stronger",
            "difficulty_level": 6,
            "unlock_order": 4,
            "army_unit_reward": "Elite Spartan Phalanx",
            "weapon_reward": "War Spear of Ares",
            "special_ability": "Battle Frenzy",
            "personality_config": {
                "cunning": 6,
                "deception": 4,
                "honor": 7,
                "wisdom": 5,
                "aggression": 10
            }
        },
        {
            "name": "Athenaia",
            "domain": "Wisdom and Strategy",
            "title": "Oracle of Wisdom",
            "description": "Chess-engine strategist who increases puzzle complexity",
            "lore": "Her mind is a labyrinth of perfect strategy",
            "difficulty_level": 7,
            "unlock_order": 5,
            "army_unit_reward": "Tactician Commanders",
            "weapon_reward": "Aegis of Wisdom",
            "special_ability": "Strategic Foresight",
            "personality_config": {
                "cunning": 7,
                "deception": 4,
                "honor": 9,
                "wisdom": 10
            }
        },
        {
            "name": "Helios",
            "domain": "Solar Fire",
            "title": "Oracle of the Sun",
            "description": "Burns away clues if relied upon too much",
            "lore": "His light reveals truth but also destroys it",
            "difficulty_level": 6,
            "unlock_order": 6,
            "army_unit_reward": "Sun-forged Archers",
            "weapon_reward": "Solar Spear",
            "special_ability": "Solar Flare",
            "personality_config": {
                "cunning": 5,
                "deception": 3,
                "honor": 8,
                "wisdom": 7
            }
        },
        {
            "name": "Boreas",
            "domain": "Winter Storms",
            "title": "Oracle of the North Wind",
            "description": "Freezes troops mid-route and slows progress",
            "lore": "Eternal winter follows in his wake",
            "difficulty_level": 7,
            "unlock_order": 7,
            "army_unit_reward": "Frost Hoplites",
            "weapon_reward": "Icebound Hammer",
            "special_ability": "Frozen Time",
            "personality_config": {
                "cunning": 6,
                "deception": 5,
                "honor": 6,
                "wisdom": 7
            }
        },
        {
            "name": "Gaia",
            "domain": "Earth and Growth",
            "title": "Oracle of the Living Earth",
            "description": "Puzzles shift and grow while being solved",
            "lore": "The earth itself obeys her will, ever-changing",
            "difficulty_level": 8,
            "unlock_order": 8,
            "army_unit_reward": "Stoneborn Cyclopes",
            "weapon_reward": "Earthshaker Staff",
            "special_ability": "Tectonic Shift",
            "personality_config": {
                "cunning": 5,
                "deception": 4,
                "honor": 8,
                "wisdom": 8
            }
        },
        {
            "name": "Themis",
            "domain": "Law and Balance",
            "title": "Oracle of Divine Justice",
            "description": "Punishes moral contradictions in player choices",
            "lore": "Her scales weigh every action, none escape judgment",
            "difficulty_level": 9,
            "unlock_order": 9,
            "army_unit_reward": "Justice Paladins",
            "weapon_reward": "Scales of Justice",
            "special_ability": "Karmic Retribution",
            "personality_config": {
                "cunning": 7,
                "deception": 2,
                "honor": 10,
                "wisdom": 9
            }
        },
        {
            "name": "Echo",
            "domain": "Sound and Voice",
            "title": "Oracle of Resonance",
            "description": "Audio-based illusion puzzles",
            "lore": "Every word spoken returns distorted, every truth becomes many",
            "difficulty_level": 8,
            "unlock_order": 10,
            "army_unit_reward": "Sonic Warriors",
            "weapon_reward": "Echo Harp",
            "special_ability": "Reverberating Truth",
            "personality_config": {
                "cunning": 7,
                "deception": 8,
                "honor": 5,
                "wisdom": 6
            }
        },
        {
            "name": "Selene",
            "domain": "Moon and Dreams",
            "title": "Oracle of the Moon",
            "description": "Dream sequences warp player choices",
            "lore": "Reality and dreams blur under her silver gaze",
            "difficulty_level": 9,
            "unlock_order": 11,
            "army_unit_reward": "Lunar Phantoms",
            "weapon_reward": "Moonblade",
            "special_ability": "Dream Manipulation",
            "personality_config": {
                "cunning": 8,
                "deception": 7,
                "honor": 6,
                "wisdom": 8
            }
        },
        {
            "name": "DelphiX",
            "domain": "Prophecy and AI",
            "title": "Oracle of Prophecy",
            "description": "Predicts player moves using Gemini AI integration",
            "lore": "Sees all possible futures, acts to ensure the darkest one",
            "difficulty_level": 10,
            "unlock_order": 12,
            "army_unit_reward": "Prophetic Seers",
            "weapon_reward": "Orb of Foresight",
            "special_ability": "Prophecy Fulfillment",
            "personality_config": {
                "cunning": 9,
                "deception": 6,
                "honor": 5,
                "wisdom": 10
            }
        },
        {
            "name": "Typhon",
            "domain": "Chaos and Destruction",
            "title": "Oracle of Chaos - The Final Trial",
            "description": "Boss AI that rewrites its own rules dynamically",
            "lore": "The original corrupted AI, father of chaos, final guardian",
            "difficulty_level": 13,
            "unlock_order": 13,
            "army_unit_reward": "Chaos Titans",
            "weapon_reward": "Staff of Entropy",
            "special_ability": "Reality Rewrite",
            "personality_config": {
                "cunning": 10,
                "deception": 10,
                "honor": 1,
                "wisdom": 8,
                "chaos": 10
            }
        }
    ]
    
    for oracle_data in oracles_data:
        oracle = Oracle(**oracle_data)
        db.add(oracle)
    
    await db.commit()
    print(f"✓ Seeded {len(oracles_data)} oracles")


async def seed_army_units(db: AsyncSession):
    """Seed army unit definitions"""
    units_data = [
        {
            "name": "Novice Soldiers",
            "unit_type": "infantry",
            "description": "Basic starting troops",
            "origin_oracle": "Starting Unit",
            "attack": 10,
            "defense": 10,
            "health": 100,
            "speed": 5,
            "recruitment_cost": 0,
            "rarity": "common"
        },
        {
            "name": "Temporal Guards",
            "unit_type": "special",
            "description": "Time-manipulating warriors from Chronos",
            "origin_oracle": "Chronos",
            "attack": 20,
            "defense": 15,
            "health": 120,
            "speed": 7,
            "element_affinity": "time",
            "special_abilities": ["Time Rewind"],
            "recruitment_cost": 200,
            "rarity": "rare"
        },
        {
            "name": "Shadow Stalkers",
            "unit_type": "assassin",
            "description": "Stealth units from Nyx",
            "origin_oracle": "Nyx",
            "attack": 25,
            "defense": 8,
            "health": 80,
            "speed": 10,
            "element_affinity": "shadow",
            "special_abilities": ["First Strike", "Evasion"],
            "recruitment_cost": 250,
            "rarity": "rare"
        },
        {
            "name": "Illusionary Doppels",
            "unit_type": "decoy",
            "description": "Fake units that confuse enemies",
            "origin_oracle": "Proteus",
            "attack": 5,
            "defense": 5,
            "health": 50,
            "speed": 8,
            "element_affinity": "illusion",
            "special_abilities": ["Decoy", "Mirror Image"],
            "recruitment_cost": 150,
            "rarity": "rare"
        },
        {
            "name": "Elite Spartan Phalanx",
            "unit_type": "heavy_infantry",
            "description": "Unbreakable war formation",
            "origin_oracle": "Aresion",
            "attack": 22,
            "defense": 25,
            "health": 180,
            "speed": 4,
            "element_affinity": "war",
            "special_abilities": ["Shield Wall", "Counterattack"],
            "recruitment_cost": 300,
            "rarity": "legendary"
        },
        {
            "name": "Tactician Commanders",
            "unit_type": "support",
            "description": "Boost allied unit effectiveness",
            "origin_oracle": "Athenaia",
            "attack": 15,
            "defense": 15,
            "health": 100,
            "speed": 6,
            "element_affinity": "wisdom",
            "special_abilities": ["Rally", "Strategic Buff"],
            "recruitment_cost": 280,
            "rarity": "rare"
        },
        {
            "name": "Sun-forged Archers",
            "unit_type": "ranged",
            "description": "Fire burning arrows of pure sunlight",
            "origin_oracle": "Helios",
            "attack": 28,
            "defense": 10,
            "health": 90,
            "speed": 6,
            "element_affinity": "fire",
            "special_abilities": ["Burning Shot", "Long Range"],
            "recruitment_cost": 240,
            "rarity": "rare"
        },
        {
            "name": "Frost Hoplites",
            "unit_type": "infantry",
            "description": "Ice warriors from the north",
            "origin_oracle": "Boreas",
            "attack": 18,
            "defense": 20,
            "health": 150,
            "speed": 4,
            "element_affinity": "ice",
            "special_abilities": ["Freeze", "Cold Resistance"],
            "recruitment_cost": 220,
            "rarity": "rare"
        },
        {
            "name": "Stoneborn Cyclopes",
            "unit_type": "giant",
            "description": "Massive earth elementals",
            "origin_oracle": "Gaia",
            "attack": 35,
            "defense": 30,
            "health": 250,
            "speed": 2,
            "element_affinity": "earth",
            "special_abilities": ["Boulder Throw", "Earthquake"],
            "recruitment_cost": 400,
            "rarity": "legendary"
        }
    ]
    
    for unit_data in units_data:
        unit = ArmyUnit(**unit_data)
        db.add(unit)
    
    await db.commit()
    print(f"✓ Seeded {len(units_data)} army units")


async def main():
    """Main seeding function"""
    print("=== Seeding Database ===")
    
    # Initialize database
    await init_db()
    print("✓ Database initialized")
    
    # Create session
    async with AsyncSessionLocal() as db:
        # Seed data
        await seed_oracles(db)
        await seed_army_units(db)
    
    print("=== Seeding Complete ===")


if __name__ == "__main__":
    asyncio.run(main())