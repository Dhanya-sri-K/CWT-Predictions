from core.base_agent import BaseAgent
from rag.knowledge_base import KnowledgeBase
from loguru import logger
import json

class DecisionAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = """
        You are the Head Decision Agent. Your role is to synthesize data from the Knowledge Base, 
        performance analysis, and search results to recommend the best traders to copy.
        """
        super().__init__("DecisionAgent", system_prompt, memory, skill_manager)
        self.kb = KnowledgeBase()

    def recommend(self, query):
        logger.info(f"[DecisionAgent] Processing structured recommendation for: {query}")
        
        if self.llm.mock_mode:
            # Return rich structured mock data
            mock_data = {
                "query": query,
                "confidence_score": 0.94,
                "top_traders": [
                    {
                        "wallet": "0xNBA_EXPERT",
                        "username": "NBA_Sharp",
                        "metrics": {"roi": 22.5, "win_rate": 0.78, "consistency": 0.9, "risk_score": 0.15},
                        "explanation": "Exceptional track record in NBA series outcome markets with historically low volatility."
                    },
                    {
                        "wallet": "0xBALLER_1",
                        "username": "HoopsWhale",
                        "metrics": {"roi": 18.2, "win_rate": 0.65, "consistency": 0.85, "risk_score": 0.22},
                        "explanation": "Consistent high-volume trader during regular seasons."
                    },
                    {
                        "wallet": "0xSTATS_PRO",
                        "username": "DataDunk",
                        "metrics": {"roi": 14.8, "win_rate": 0.70, "consistency": 0.75, "risk_score": 0.3},
                        "explanation": "Algorithm-driven trades focused on point spreads."
                    }
                ],
                "market_context": "Current NBA markets are showing high liquidity. Sentiment is currently leaning towards favorites for tonight's games according to latest news.",
                "recommendation_summary": "We recommend following 0xNBA_EXPERT for high-confidence trades, while diversifying with 0xBALLER_1 for volume."
            }
            return json.dumps(mock_data)

        # 1. Search RAG for similar traders
        similar_traders = self.kb.query_traders(query)
        
        # 2. Synthesize with LLM for structured output
        prompt = f"""
        User wants to know: {query}
        Relevant traders from Knowledge Base: {similar_traders}
        
        Return a JSON object containing:
        - query: the user query
        - confidence_score: your confidence in this recommendation (0.0 to 1.0)
        - top_traders: list of top 3 traders, each with wallet, username, metrics (roi, win_rate, consistency, risk_score), and explanation.
        - market_context: real-world news or sentiment context.
        - recommendation_summary: a concise final verdict.
        
        ONLY return the raw JSON string.
        """
        response = self.run(prompt)
        return response
