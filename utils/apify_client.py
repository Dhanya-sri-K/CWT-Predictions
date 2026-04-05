import os
from loguru import logger
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

class ApifyWrapper:
    def __init__(self):
        self.token = os.getenv("APIFY_API_TOKEN")
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        if not self.mock_mode:
            self.client = ApifyClient(self.token)

    def run_actor(self, actor_id, run_input):
        if self.mock_mode:
            logger.info(f"[Mock] Apify running actor: {actor_id}")
            if "leaderboard" in actor_id:
                return [
                    {"proxy": "0xNBA_EXPERT", "profit": 250000, "username": "NBA_Sharp"},
                    {"proxy": "0xPOLITICS_WHALE", "profit": 300000, "username": "DCPundit"},
                    {"proxy": "0xWEATHER_GOD", "profit": 150000, "username": "CloudChaser"}
                ]
            return [{"title": "NBA Market Trends", "url": "https://kalshi.com/nba"}]
        
        run = self.client.actor(actor_id).call(run_input=run_input)
        run = self.client.actor(actor_id).call(run_input=run_input)
        return list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

    def search_polymarket_leaderboard(self, time_range="all", leaderboard_type="profit"):
        """
        Uses saswave/polymarket-leaderboard-scraper
        """
        run_input = {
            "timeRange": time_range,
            "type": leaderboard_type
        }
        return self.run_actor("saswave/polymarket-leaderboard-scraper", run_input)

    def search_kalshi_markets(self, limit=10):
        """
        Uses a generic Kalshi scraper or search
        """
        # Using a representative actor if one exists or fallback
        # For now, let's assume a generic one or search
        run_input = {
            "limit": limit
        }
        return self.run_actor("apify/google-search-scraper", {"queries": ["site:kalshi.com markets"]})
