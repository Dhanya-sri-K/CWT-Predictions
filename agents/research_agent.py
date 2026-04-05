import os
from core.base_agent import BaseAgent
from utils.apify_client import ApifyWrapper
from loguru import logger

class ResearchAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are a research agent that enriches RAG by searching for real-world context using Apify.
        Your goal is to find the latest news and data related to specific events being traded on prediction markets.
        """
        super().__init__("ResearchAgent", system_prompt, memory, skill_manager)
        self.apify = ApifyWrapper()

    def enrich_event(self, event_name):
        logger.info(f"[ResearchAgent] Enriching event: {event_name}")
        
        # Trigger Search
        search_results = self.apify.run_actor("apify/google-search-scraper", {"queries": [f"latest news about {event_name}"]})
        
        # Process and summarize
        summary = f"Gathered research data for {event_name}."
        if search_results:
            summary += "\nFound the following context:\n"
            for res in search_results[:3]:
                summary += f"- {res.get('title')}: {res.get('description') or res.get('url')}\n"
        
        # Learning Loop
        self.learn("Enrichment Task", f"Used google-search-scraper for 'latest news about {event_name}'.")
        
        return summary, search_results
