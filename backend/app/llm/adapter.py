### File: backend/app/llm/adapter.py
"""
backend/app/llm/adapter.py
STEP: LLM Adapter for Ollama/vLLM
Unified interface for local LLM inference using Ollama or vLLM.
"""
import httpx
import json
from typing import Dict, Any, List, Optional
from app.config import settings


class LLMAdapter:
    """Unified adapter for Ollama/vLLM inference"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.DEFAULT_LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system: Optional[str] = None,
        json_mode: bool = False
    ) -> str:
        """
        Generate completion from LLM.
        STEP: Sends prompt to Ollama, returns generated text.
        """
        model = model or self.default_model
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if json_mode:
            payload["format"] = "json"
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            print(f"LLM generation error: {e}")
            raise Exception(f"LLM call failed: {e}")
    
    async def generate_with_context(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate with conversation context.
        STEP: Supports multi-turn conversations with message history.
        """
        model = model or self.default_model
        temperature = temperature or self.temperature
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": self.max_tokens
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            print(f"LLM generation error: {e}")
            raise Exception(f"LLM call failed: {e}")
    
    async def embed_text(self, text: str, model: str = "nomic-embed-text") -> List[float]:
        """
        Generate embeddings for text.
        STEP: Creates vector embeddings for semantic search.
        """
        payload = {
            "model": model,
            "prompt": text
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/embeddings",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["embedding"]
        except Exception as e:
            print(f"Embedding error: {e}")
            raise Exception(f"Embedding failed: {e}")
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
