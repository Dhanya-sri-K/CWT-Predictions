import os
import sys
from dotenv import load_dotenv
from loguru import logger

from core.memory import PersistentMemory
from core.skill_manager import SkillManager
from rag.knowledge_base import KnowledgeBase

from agents.polymarket_agent import PolymarketAgent
from agents.v2.analyzer_agent import AnalyzerAgent
from agents.v2.niche_agent import NicheAgent
from agents.v2.decision_agent import DecisionAgent
from agents.v2.enrichment_agent import EnrichmentAgent
from agents.v2.learning_agent import LearningAgent

def run_advanced_flow(query):
    load_dotenv()
    
    # 1. Initialization
    memory = PersistentMemory()
    skill_manager = SkillManager()
    kb = KnowledgeBase()
    
    # 2. Agent Suite
    poly_agent = PolymarketAgent(memory, skill_manager)
    analyzer = AnalyzerAgent(memory, skill_manager)
    niche_agent = NicheAgent(memory, skill_manager)
    enricher = EnrichmentAgent(memory, skill_manager)
    decision_agent = DecisionAgent(memory, skill_manager)
    learning_agent = LearningAgent(memory, skill_manager, kb)

    print(f"\n--- Processing Query: {query} ---\n")

    # 3. Discovery & Prep (Example: Discover and Rank)
    print("[1/4] Discovering Traders...")
    summary, traders = poly_agent.discover_traders()
    
    print("[2/4] Analyzing & Mapping Niches...")
    for trader in traders[:3]:
        # Analyze performance
        stats = analyzer.analyze_trader({"wallet": trader.get('proxy'), "roi": trader.get('profit', 0)/100000, "trades": []})
        
        # Classify niche
        niche = niche_agent.classify(f"Trader {trader.get('proxy')} with profit {trader.get('profit')}")
        
        # Store in RAG Knowledge Base
        kb.add_trader_profile(trader.get('proxy'), stats, niche)

    # 4. Enrichment
    print("[3/4] Enriching Context with External Sentiment...")
    enrichment = enricher.enrich(query)
    print(f"Sentiment Analysis: {enrichment['analysis'][:100]}...")

    # 5. Final Decision
    print("[4/4] Generating Recommendation...")
    recommendation = decision_agent.recommend(f"{query}. Context: {enrichment['analysis']}")
    
    print("\n--- FINAL RECOMMENDATION ---")
    print(recommendation)
    
    # 6. Learning Loop (Verification placeholder)
    print("\n[Learning Loop] Running Hermes Reflection...")
    learning_agent.verify_outcome("Sample_Wallet", "Bullish", "Bullish")

if __name__ == "__main__":
    q = "Who is the most consistent NBA trader to follow for today's games?"
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
    run_advanced_flow(q)
