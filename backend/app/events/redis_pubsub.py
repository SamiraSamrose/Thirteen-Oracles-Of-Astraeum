### File: backend/app/events/redis_pubsub.py

"""
backend/app/events/redis_pubsub.py
STEP: Redis Pub/Sub for Agent Communication
Enables real-time agent event subscription and broadcasting.
"""
import redis.asyncio as redis
import json
from typing import Callable, Dict, Any
import asyncio

from app.config import settings


class RedisPubSub:
    """Redis-based pub/sub for agent communication"""
    
    def __init__(self):
        self.redis_client = None
        self.pubsub = None
        self.subscribers: Dict[str, list] = {}
    
    async def connect(self):
        """
        Connect to Redis.
        STEP: Establishes Redis connection for pub/sub.
        """
        self.redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
    
    async def publish(self, channel: str, message: Dict[str, Any]):
        """
        Publish message to channel.
        STEP: Broadcasts event to all subscribers on channel.
        """
        if not self.redis_client:
            await self.connect()
        
        message_json = json.dumps(message)
        await self.redis_client.publish(channel, message_json)
    
    async def subscribe(self, channel: str, callback: Callable):
        """
        Subscribe to channel with callback.
        STEP: Registers callback for messages on channel.
        """
        if not self.pubsub:
            await self.connect()
        
        await self.pubsub.subscribe(channel)
        
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)
    
    async def listen(self):
        """
        Listen for messages on subscribed channels.
        STEP: Async loop processing incoming messages.
        """
        if not self.pubsub:
            await self.connect()
        
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                channel = message["channel"]
                data = json.loads(message["data"])
                
                # Call all callbacks for this channel
                if channel in self.subscribers:
                    for callback in self.subscribers[channel]:
                        try:
                            await callback(data)
                        except Exception as e:
                            print(f"Error in subscriber callback: {e}")
    
    async def close(self):
        """Close connections"""
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()
