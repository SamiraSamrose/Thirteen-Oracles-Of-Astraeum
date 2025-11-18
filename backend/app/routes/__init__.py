## STEP 8: API ROUTES

### File: backend/app/routes/__init__.py

"""
backend/app/routes/__init__.py
API routes package
"""
from fastapi import APIRouter

from app.routes import auth, game, oracle, assets

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(game.router, prefix="/game", tags=["game"])
api_router.include_router(oracle.router, prefix="/oracle", tags=["oracle"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
