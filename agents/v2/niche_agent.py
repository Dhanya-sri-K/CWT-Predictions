from core.base_agent import BaseAgent
from loguru import logger

class NicheAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are a Niche Classification Specialist. You classify traders based on their history 
        into categories: NBA, Politics, Economics, Weather, Pop Culture, etc.
        """
        super().__init__("NicheAgent", system_prompt, memory, skill_manager)

    def classify(self, trader_data):
        logger.info(f"[NicheAgent] Classifying trader data...")
        
        prompt = f"Based on this trade history, identify the primary niche and confidence level: {trader_data}"
        classification = self.run(prompt)
        
        return classification
