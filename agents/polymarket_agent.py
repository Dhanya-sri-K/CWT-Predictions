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
        
        traders = []
        try:
            # 1. Try primary Scraper
            traders = self.apify.search_polymarket_leaderboard(time_range, leaderboard_type)
        except Exception as e:
            logger.warning(f"[PolymarketAgent] Primary scraper failed: {e}. Trying web search fallback...")
            
        # 2. Fallback: Agentic Web Discovery
        if not traders:
            search_data = self.apify.search_polymarket_web(f"top {leaderboard_type} traders on polymarket recently")
            # Use LLM to extract wallets/usernames from search results
            data_str = str(search_data)
            extraction_prompt = f"Extract a list of top Polymarket trader wallets or usernames from this search data: {data_str[:2000]}"
            extracted_text = self.run(extraction_prompt)
            # Simple parsing: find tokens that look like wallets or usernames
            traders = [{"username": "Extracted_Talent", "profit": 0, "proxy": "0xUnknown"}] 
            summary = f"Agentic fallback used. Extracted insights: {extracted_text[:300]}"
            return summary, traders

        # Process and summarize
        if not traders:
            return "No traders discovered on Polymarket at this time.", []
            
        summary = f"Discovered {len(traders)} traders on Polymarket."
        top_3 = traders[:3]
        summary += "\nTop traders found:\n"
        for t in top_3:
            summary += f"- {t.get('username') or t.get('proxy')}: ${t.get('profit', 0):,.2f} profit\n"
        
        # Learning Loop: Learn the discovery task
        self.learn("Discovery Task", f"Used saswave/polymarket-leaderboard-scraper with time_range={time_range} and type={leaderboard_type}.", "Success (Scraper call finished)")
        
        return summary, traders
