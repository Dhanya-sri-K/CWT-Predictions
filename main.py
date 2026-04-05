import os
import sys
from dotenv import load_dotenv
from loguru import logger

from core.memory import PersistentMemory
from core.skill_manager import SkillManager
from agents.polymarket_agent import PolymarketAgent
from agents.kalshi_agent import KalshiAgent
from agents.niche_mapper_agent import NicheMapperAgent
from agents.research_agent import ResearchAgent

# Configure Logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/agent.log", rotation="10 MB", level="DEBUG")

def main():
    load_dotenv()
    
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("APIFY_API_TOKEN"):
        logger.warning("Missing API keys in .env. Please check .env.template.")

    # Initialize Core Components
    memory = PersistentMemory()
    skill_manager = SkillManager()
    
    # Initialize Agents
    poly_agent = PolymarketAgent(memory, skill_manager)
    kalshi_agent = KalshiAgent(memory, skill_manager)
    niche_agent = NicheMapperAgent(memory, skill_manager)
    research_agent = ResearchAgent(memory, skill_manager)

    print("\n" + "="*50)
    print("Welcome to the Prediction Market Research Tool")
    print("Agent Framework: Hermes-Inspired (Closed Learning Loop)")
    print("="*50 + "\n")

    while True:
        user_input = input("\n[User] (Type 'exit' to quit) > ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        
        # Simple Logic to route or execute steps
        if "polymarket" in user_input.lower() or "traders" in user_input.lower():
            print("\n[PolymarketAgent] Searching for top traders...")
            summary, traders = poly_agent.discover_traders()
            print(summary)
            
            do_map = input("\nMap these traders to niches? (y/n) > ").strip().lower()
            if do_map == 'y':
                niche_info = niche_agent.map_to_niche(traders)
                print(f"\n[NicheMapperAgent] Analysis:\n{niche_info}")
                
        elif "kalshi" in user_input.lower():
            print("\n[KalshiAgent] Searching for active markets...")
            summary, markets = kalshi_agent.search_markets()
            print(summary)
            
        elif "research" in user_input.lower() or "enrich" in user_input.lower():
            event = input("\nWhat event should I research? > ")
            summary, context = research_agent.enrich_event(event)
            print(summary)
            
        else:
            # Generic chat with the research agent or others
            response = research_agent.run(user_input)
            print(f"\n[Assistant] {response}")

if __name__ == "__main__":
    main()
