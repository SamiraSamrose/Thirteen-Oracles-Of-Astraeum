### File: backend/app/events/kafka_consumer.py

"""
backend/app/events/kafka_consumer.py
STEP: Kafka Event Consumer
Consumes game events for agent reactions and analytics.
"""
from aiokafka import AIOKafkaConsumer
import json
import asyncio

from app.config import settings


class KafkaEventConsumer:
    """Kafka consumer for processing game events"""
    
    def __init__(self, orchestrator=None):
        self.consumer = None
        self.orchestrator = orchestrator
        self.running = False
    
    async def start(self):
        """
        Start Kafka consumer.
        STEP: Connects to Kafka and begins consuming events.
        """
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC_GAME_EVENTS,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='astraeum-agents'
        )
        await self.consumer.start()
        self.running = True
    
    async def consume_events(self):
        """
        Consume and process events.
        STEP: Async loop processing Kafka messages and routing to orchestrator.
        """
        if not self.consumer:
            await self.start()
        
        try:
            async for message in self.consumer:
                if not self.running:
                    break
                
                event = message.value
                event_type = event.get("type")
                event_data = event.get("data")
                
                # Route to orchestrator
                if self.orchestrator:
                    try:
                        await self.orchestrator.route_event(event_type, event_data)
                    except Exception as e:
                        print(f"Error processing event {event_type}: {e}")
        
        except Exception as e:
            print(f"Error in Kafka consumer: {e}")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop consumer"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()


async def start_kafka_consumer(orchestrator):
    """
    Start Kafka consumer in background.
    STEP: Launches consumer as background task.
    """
    consumer = KafkaEventConsumer(orchestrator)
    asyncio.create_task(consumer.consume_events())
    return consumer
