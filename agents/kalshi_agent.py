from core.base_agent import BaseAgent
from utils.apify_client import ApifyWrapper
from loguru import logger

class KalshiAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are an expert in Kalshi prediction markets. 
        Your goal is to identify high-volume markets and the traders who consistently predict outcomes correctly.
        """
        super().__init__("KalshiAgent", system_prompt, memory, skill_manager)
        self.apify = ApifyWrapper()

    def search_markets(self, limit=5):
        logger.info(f"[KalshiAgent] Searching for active markets (limit: {limit})")
        
        # Trigger generic search or scraper
        results = self.apify.search_kalshi_markets(limit)
        
        # Summarize results
        summary = f"Identified {len(results)} active markets or mentions on Kalshi."
        if results:
            summary += "\nFound the following Kalshi data:\n"
            for r in results[:limit]:
                summary += f"- {r.get('title')}: {r.get('url')}\n"
        
        # Learning Loop: Learn search strategy
        self.learn("Market Search", f"Used google-search-scraper for 'site:kalshi.com markets' with limit={limit}.")
        
        return summary, results
