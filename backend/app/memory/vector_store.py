### File: backend/app/memory/vector_store.py

"""
backend/app/memory/vector_store.py
STEP: Weaviate Vector Memory Integration
Stores agent memories, player patterns, and context for semantic retrieval.
"""
import weaviate
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.config import settings


class VectorMemory:
    """Weaviate-based vector memory for agent learning"""
    
    def __init__(self):
        """Initialize Weaviate client"""
        auth_config = None
        if settings.WEAVIATE_API_KEY:
            auth_config = weaviate.AuthApiKey(api_key=settings.WEAVIATE_API_KEY)
        
        self.client = weaviate.Client(
            url=settings.WEAVIATE_URL,
            auth_client_secret=auth_config
        )
        self._create_schema()
    
    def _create_schema(self):
        """
        Create Weaviate schema for agent memories.
        STEP: Defines memory structure with vector embeddings.
        """
        schema = {
            "classes": [
                {
                    "class": "AgentMemory",
                    "description": "Oracle agent memories and learned patterns",
                    "vectorizer": "text2vec-transformers",
                    "properties": [
                        {
                            "name": "oracle_name",
                            "dataType": ["string"],
                            "description": "Which oracle this memory belongs to"
                        },
                        {
                            "name": "memory_type",
                            "dataType": ["string"],
                            "description": "Type: player_pattern, tactic, conversation, event"
                        },
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "Memory content"
                        },
                        {
                            "name": "context",
                            "dataType": ["text"],
                            "description": "Additional context"
                        },
                        {
                            "name": "importance",
                            "dataType": ["number"],
                            "description": "Memory importance score 0-1"
                        },
                        {
                            "name": "timestamp",
                            "dataType": ["date"],
                            "description": "When memory was created"
                        },
                        {
                            "name": "metadata",
                            "dataType": ["text"],
                            "description": "JSON metadata"
                        }
                    ]
                },
                {
                    "class": "PlayerPattern",
                    "description": "Learned player behavior patterns",
                    "vectorizer": "text2vec-transformers",
                    "properties": [
                        {
                            "name": "player_id",
                            "dataType": ["string"],
                            "description": "Player identifier"
                        },
                        {
                            "name": "pattern_type",
                            "dataType": ["string"],
                            "description": "combat_style, puzzle_approach, diplomacy_preference"
                        },
                        {
                            "name": "description",
                            "dataType": ["text"],
                            "description": "Pattern description"
                        },
                        {
                            "name": "frequency",
                            "dataType": ["number"],
                            "description": "How often pattern appears"
                        },
                        {
                            "name": "confidence",
                            "dataType": ["number"],
                            "description": "Confidence in pattern 0-1"
                        },
                        {
                            "name": "timestamp",
                            "dataType": ["date"],
                            "description": "Last observed"
                        }
                    ]
                }
            ]
        }
        
        try:
            # Try to create schema (will skip if exists)
            self.client.schema.create(schema)
        except Exception as e:
            print(f"Schema creation note: {e}")
    
    async def store_memory(
        self,
        oracle_name: str,
        memory_type: str,
        content: str,
        context: str = "",
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Store agent memory with embedding.
        STEP: Saves memory to Weaviate with automatic vectorization.
        """
        import json
        
        data_object = {
            "oracle_name": oracle_name,
            "memory_type": memory_type,
            "content": content,
            "context": context,
            "importance": importance,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": json.dumps(metadata or {})
        }
        
        try:
            result = self.client.data_object.create(
                data_object,
                "AgentMemory"
            )
            return result
        except Exception as e:
            print(f"Error storing memory: {e}")
            return None
    
    async def retrieve_relevant_memories(
        self,
        oracle_name: str,
        query: str,
        limit: int = 5,
        min_importance: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve semantically similar memories.
        STEP: Uses vector similarity search to find relevant past experiences.
        """
        try:
            result = (
                self.client.query
                .get("AgentMemory", ["oracle_name", "memory_type", "content", "context", "importance", "timestamp"])
                .with_near_text({"concepts": [query]})
                .with_where({
                    "operator": "And",
                    "operands": [
                        {
                            "path": ["oracle_name"],
                            "operator": "Equal",
                            "valueString": oracle_name
                        },
                        {
                            "path": ["importance"],
                            "operator": "GreaterThanEqual",
                            "valueNumber": min_importance
                        }
                    ]
                })
                .with_limit(limit)
                .do()
            )
            
            if "data" in result and "Get" in result["data"]:
                return result["data"]["Get"]["AgentMemory"]
            return []
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    async def store_player_pattern(
        self,
        player_id: str,
        pattern_type: str,
        description: str,
        frequency: float,
        confidence: float
    ) -> str:
        """
        Store learned player behavior pattern.
        STEP: Records player tendencies for agent adaptation.
        """
        data_object = {
            "player_id": str(player_id),
            "pattern_type": pattern_type,
            "description": description,
            "frequency": frequency,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            result = self.client.data_object.create(
                data_object,
                "PlayerPattern"
            )
            return result
        except Exception as e:
            print(f"Error storing pattern: {e}")
            return None
    
    async def get_player_patterns(
        self,
        player_id: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all learned patterns for a player.
        STEP: Gets player behavioral profile for agent decision-making.
        """
        try:
            result = (
                self.client.query
                .get("PlayerPattern", ["player_id", "pattern_type", "description", "frequency", "confidence"])
                .with_where({
                    "path": ["player_id"],
                    "operator": "Equal",
                    "valueString": str(player_id)
                })
                .do()
            )
            
            if "data" in result and "Get" in result["data"]:
                return result["data"]["Get"]["PlayerPattern"]
            return []
        except Exception as e:
            print(f"Error retrieving patterns: {e}")
            return []
