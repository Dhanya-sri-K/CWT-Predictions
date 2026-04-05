from core.base_agent import BaseAgent
from utils.apify_client import ApifyWrapper
from loguru import logger

class EnrichmentAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are an Enrichment & Sentiment Agent. You use Apify to scrape current news 
        and Twitter sentiment to provide context for prediction market events.
        """
        super().__init__("EnrichmentAgent", system_prompt, memory, skill_manager)
        self.apify = ApifyWrapper()

    def enrich(self, event_description):
        logger.info(f"[EnrichmentAgent] Fetching external context for: {event_description}")
        
        # 1. Search News
        search_results = self.apify.run_actor("apify/google-search-scraper", {"queries": [f"sentiment and news on {event_description}"]})
        
        # 2. Extract Sentiment (Mock logic for demonstration)
        analysis = self.run(f"Analyze the sentiment of these search results for the event '{event_description}': {search_results[:3]}")
        
        return {
            "analysis": analysis,
            "raw_results": search_results[:3]
        }
