from core.base_agent import BaseAgent
from loguru import logger

class NicheMapperAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are an expert at mapping prediction market traders to specific niches like NBA, Politics, Weather, and Crypto. 
        Analyze trade history and market descriptions to categorize wallets.
        """
        super().__init__("NicheMapperAgent", system_prompt, memory, skill_manager)

    def map_to_niche(self, traders_data):
        logger.info("[NicheMapperAgent] Mapping traders to niches...")
        
        # LLM Analyze the data
        analysis_prompt = f"Categorize the following trader data into niches (NBA/Politics/Weather/etc.):\n\n{traders_data}"
        niche_mapping = self.run(analysis_prompt)
        
        # Learning Loop
        self.learn("Niche Mapping", "Analyzed trader profiles and transaction history to infer categories.")
        
        return niche_mapping
