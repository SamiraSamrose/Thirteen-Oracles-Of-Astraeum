### File: backend/app/events/kafka_producer.py

"""
backend/app/events/kafka_producer.py
STEP: Kafka Event Producer
Publishes game events to Kafka for agent consumption and analytics.
"""
from aiokafka import AIOKafkaProducer
import json
from typing import Dict, Any

from app.config import settings


class KafkaEventProducer:
    """Kafka producer for game events"""
    
    def __init__(self):
        self.producer = None
    
    async def start(self):
        """
        Start Kafka producer.
        STEP: Initializes connection to Kafka broker.
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
    
    async def send_game_event(
        self,
        event_type: str,
        event_data: Dict[str, Any]
    ):
        """
        Send game event to Kafka.
        STEP: Publishes event to game-events topic for agent processing.
        """
        if not self.producer:
            await self.start()
        
        event = {
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.producer.send(
            settings.KAFKA_TOPIC_GAME_EVENTS,
            value=event
        )
    
    async def send_agent_action(
        self,
        oracle_name: str,
        action_type: str,
        action_data: Dict[str, Any]
    ):
        """
        Send agent action to Kafka.
        STEP: Publishes agent decisions for logging and processing.
        """
        if not self.producer:
            await self.start()
        
        action = {
            "oracle": oracle_name,
            "action_type": action_type,
            "action_data": action_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.producer.send(
            settings.KAFKA_TOPIC_AGENT_ACTIONS,
            value=action
        )
    
    async def stop(self):
        """Stop producer"""
        if self.producer:
            await self.producer.stop()
