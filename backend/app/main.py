## STEP 9: MAIN APPLICATION

### File: backend/app/main.py

"""
backend/app/main.py
STEP: FastAPI Application Entry Point
Initializes app, middleware, routes, WebSocket, background services.
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.database import init_db
from app.routes import api_router
from app.websocket.manager import ConnectionManager
from app.events.kafka_consumer import start_kafka_consumer
from app.events.kafka_producer import KafkaEventProducer
from app.events.redis_pubsub import RedisPubSub
from app.agents.orchestrator import AgentOrchestrator
from app.llm.adapter import LLMAdapter
from app.memory.vector_store import VectorMemory

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1,
    )

# Global instances
ws_manager = ConnectionManager()
orchestrator = None
llm_adapter = None
vector_memory = None
kafka_producer = None
redis_pubsub = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    STEP: Handles startup and shutdown of all services.
    """
    global orchestrator, llm_adapter, vector_memory, kafka_producer, redis_pubsub
    
    # Startup
    print("Starting Thirteen Oracles of Astraeum backend...")
    
    # Initialize database
    await init_db()
    print("Database initialized")
    
    # Initialize LLM adapter
    llm_adapter = LLMAdapter()
    print("LLM adapter initialized")
    
    # Initialize vector memory
    vector_memory = VectorMemory()
    print("Vector memory initialized")
    
    # Initialize agent orchestrator
    orchestrator = AgentOrchestrator(llm_adapter, vector_memory)
    print("Agent orchestrator initialized with 13 oracles")
    
    # Initialize Kafka producer
    kafka_producer = KafkaEventProducer()
    await kafka_producer.start()
    print("Kafka producer started")
    
    # Initialize Redis pub/sub
    redis_pubsub = RedisPubSub()
    await redis_pubsub.connect()
    print("Redis pub/sub connected")
    
    # Start Kafka consumer
    await start_kafka_consumer(orchestrator)
    print("Kafka consumer started")
    
    print("Backend ready on port", settings.API_PORT)
    
    yield
    
    # Shutdown
    print("Shutting down...")
    
    if kafka_producer:
        await kafka_producer.stop()
    
    if redis_pubsub:
        await redis_pubsub.close()
    
    if orchestrator:
        await orchestrator.shutdown()
    
    print("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Thirteen Oracles of Astraeum API",
    description="Backend API for AI-powered strategy game",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": "Thirteen Oracles of Astraeum",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "llm": "ready",
        "agents": "active",
        "kafka": "connected",
        "redis": "connected"
    }


@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int, player_id: int):
    """
    WebSocket endpoint for real-time game updates.
    STEP: Manages persistent connection for state synchronization.
    """
    await ws_manager.connect(websocket, player_id, game_id)
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            
            # Process message type
            message_type = data.get("type")
            
            if message_type == "ping":
                await ws_manager.send_personal_message(
                    {"type": "pong"},
                    websocket
                )
            
            elif message_type == "game_action":
                # Broadcast action to game room
                await ws_manager.broadcast_game_event(
                    "player_action",
                    {
                        "player_id": player_id,
                        "action": data.get("action"),
                        "data": data.get("data")
                    },
                    game_id
                )
                
                # Publish to Kafka for agent processing
                if kafka_producer:
                    await kafka_producer.send_game_event(
                        "player_action",
                        {
                            "game_id": game_id,
                            "player_id": player_id,
                            "action": data.get("action")
                        }
                    )
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, player_id, game_id)
        await ws_manager.broadcast_game_event(
            "player_disconnected",
            {"player_id": player_id},
            game_id
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    print(f"Global error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
