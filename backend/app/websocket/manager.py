### File: backend/app/websocket/manager.py

"""
backend/app/websocket/manager.py
STEP: WebSocket Connection Manager
Manages real-time WebSocket connections for game state synchronization.
"""
from fastapi import WebSocket
from typing import Dict, Set
import json
import asyncio


class ConnectionManager:
    """
    Manages WebSocket connections for real-time game updates.
    STEP: Handles connection lifecycle, broadcasting, per-player routing.
    """
    
    def __init__(self):
        # player_id -> Set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # game_id -> Set of player_ids
        self.game_rooms: Dict[int, Set[int]] = {}
    
    async def connect(self, websocket: WebSocket, player_id: int, game_id: int):
        """
        Accept new WebSocket connection.
        STEP: Registers connection, joins game room.
        """
        await websocket.accept()
        
        if player_id not in self.active_connections:
            self.active_connections[player_id] = set()
        self.active_connections[player_id].add(websocket)
        
        if game_id not in self.game_rooms:
            self.game_rooms[game_id] = set()
        self.game_rooms[game_id].add(player_id)
        
        # Send connection confirmation
        await self.send_personal_message(
            {"type": "connected", "player_id": player_id, "game_id": game_id},
            websocket
        )
    
    def disconnect(self, websocket: WebSocket, player_id: int, game_id: int):
        """
        Remove WebSocket connection.
        STEP: Cleans up connection and room membership.
        """
        if player_id in self.active_connections:
            self.active_connections[player_id].discard(websocket)
            if not self.active_connections[player_id]:
                del self.active_connections[player_id]
        
        if game_id in self.game_rooms:
            self.game_rooms[game_id].discard(player_id)
            if not self.game_rooms[game_id]:
                del self.game_rooms[game_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except:
            pass
    
    async def send_to_player(self, message: dict, player_id: int):
        """
        Send message to all connections of a player.
        STEP: Broadcasts to player across all their devices/tabs.
        """
        if player_id in self.active_connections:
            disconnected = set()
            for websocket in self.active_connections[player_id]:
                try:
                    await websocket.send_json(message)
                except:
                    disconnected.add(websocket)
            
            # Clean up disconnected sockets
            for websocket in disconnected:
                self.active_connections[player_id].discard(websocket)
    
    async def broadcast_to_game(self, message: dict, game_id: int):
        """
        Broadcast message to all players in a game.
        STEP: Sends update to everyone in game room (for multiplayer).
        """
        if game_id in self.game_rooms:
            for player_id in self.game_rooms[game_id]:
                await self.send_to_player(message, player_id)
    
    async def broadcast_game_event(
        self,
        event_type: str,
        event_data: dict,
        game_id: int
    ):
        """
        Broadcast game event to all players.
        STEP: Sends structured event updates in real-time.
        """
        message = {
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_game(message, game_id)
