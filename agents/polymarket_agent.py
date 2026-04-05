from core.base_agent import BaseAgent
from utils.apify_client import ApifyWrapper
from loguru import logger

class PolymarketAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are an expert in Polymarket prediction markets. 
        Your goal is to find consistent, high-performing traders and analyze their patterns.
        Use the available data to identify wallets with high profit or volume.
        """
        super().__init__("PolymarketAgent", system_prompt, memory, skill_manager)
        self.apify = ApifyWrapper()

    def discover_traders(self, time_range="all", leaderboard_type="profit"):
        logger.info(f"[PolymarketAgent] Beginning trader discovery (type: {leaderboard_type}, range: {time_range})")
        
        # Trigger Apify actor
        traders = self.apify.search_polymarket_leaderboard(time_range, leaderboard_type)
        
        # Process and summarize
        summary = f"Discovered {len(traders)} traders on Polymarket."
        if traders:
            top_3 = traders[:3]
            summary += "\nTop traders found:\n"
            for t in top_3:
                summary += f"- {t.get('username') or t.get('proxy')}: ${t.get('profit', 0):,.2f} profit\n"
        
        # Learning Loop: Learn the discovery task
        self.learn("Discovery Task", f"Used saswave/polymarket-leaderboard-scraper with time_range={time_range} and type={leaderboard_type}.")
        
        return summary, traders
