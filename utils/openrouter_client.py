import os
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct:free")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"

    def complete(self, messages, temperature=0.7):
        if self.mock_mode:
            logger.info("[Mock] OpenRouter returning dummy response")
            return "Based on the consistent performance in NBA markets, Wallet_A is highly recommended. The trader has a 22% ROI and maintains a low risk score by hedging on high-variance games."
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/nousresearch/hermes-agent", # Dummy referer
            "X-Title": "Hermes Agent Framework",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
