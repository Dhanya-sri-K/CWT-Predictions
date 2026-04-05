import os
from loguru import logger
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "openrouter/free")
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        
        if not self.mock_mode:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )

    def complete(self, messages, temperature=0.7):
        if self.mock_mode:
            logger.info("[Mock] OpenRouter returning dummy response")
            return "Based on the consistent performance in NBA markets, Wallet_A is highly recommended. The trader has a 22% ROI and maintains a low risk score by hedging on high-variance games."
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/nousresearch/hermes-agent",
                    "X-Title": "Prediction Market Intelligence",
                },
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenRouter Error: {e}")
            raise
