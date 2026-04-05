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
        return list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

    def search_polymarket_leaderboard(self, time_range="all", leaderboard_type="profit"):
        """
        Uses saswave/polymarket-leaderboard-scraper
        Fixed input mapping based on actor schema
        """
        # Map to actor specific values
        type_map = {"profit": "PNL", "volume": "VOL"}
        
        # leaderboard_rangedate: all, month, week, day
        actor_range = time_range.lower() if time_range.lower() in ["all", "month", "week", "day"] else "all"
        actor_type = type_map.get(leaderboard_type.lower(), "PNL")

        run_input = {
            "leaderboard_rangedate": actor_range,
            "leaderboard_section": actor_type,
            "max_results": 10,
            "leaderboard_categories": "overall"
        }
        return self.run_actor("saswave/polymarket-leaderboard-scraper", run_input)

    def search_polymarket_web(self, query="top traders on polymarket"):
        """
        Robust fallback: Search the web and extract trader info
        """
        logger.info(f"[ApifyWrapper] Using web search fallback for discovery: {query}")
        return self.run_actor("apify/google-search-scraper", {"queries": query})

    def search_polymarket_leaderboard(self, time_range="all", leaderboard_type="profit"):
        """
        Uses saswave/polymarket-leaderboard-scraper
        Fixed input mapping based on actor schema
        """
        # Map to actor specific values
        type_map = {"profit": "PNL", "volume": "VOL"}
        
        # leaderboard_rangedate: all, month, week, day
        actor_range = time_range.lower() if time_range.lower() in ["all", "month", "week", "day"] else "all"
        actor_type = type_map.get(leaderboard_type.lower(), "PNL")

        run_input = {
            "leaderboard_rangedate": actor_range,
            "leaderboard_section": actor_type,
            "max_results": 10,
            "leaderboard_categories": "overall"
        }
        return self.run_actor("saswave/polymarket-leaderboard-scraper", run_input)
