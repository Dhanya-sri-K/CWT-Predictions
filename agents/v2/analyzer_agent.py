from core.base_agent import BaseAgent
from services.scoring import ScoringService
from loguru import logger

class AnalyzerAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None):
        system_prompt = "You analyze trader performance data to compute advanced risk and return metrics."
        super().__init__("AnalyzerAgent", system_prompt, memory, skill_manager)

    def analyze_trader(self, wallet_data):
        """
        wallet_data: dict with 'trades', 'roi', etc.
        """
        returns = [t.get('profit', 0) for t in wallet_data.get('trades', [])]
        roi = wallet_data.get('roi', 0.0)
        consistency = 0.5 # Default logic if not enough trades
        if len(returns) > 5:
            # Simple consistency: percentage of positive returns
            pos_returns = [r for r in returns if r > 0]
            consistency = len(pos_returns) / len(returns)
        
        risk = 1.0 - consistency # Simple inverse
        
        # Calculate scores
        score = ScoringService.calculate_trader_score(
            roi=roi, 
            consistency=consistency, 
            niche_accuracy=0.7, # Default until niche agent refines 
            risk=risk
        )
        
        logger.info(f"[AnalyzerAgent] Wallet {wallet_data.get('wallet')} score: {score}")
        
        return {
            "wallet": wallet_data.get('wallet'),
            "roi": roi,
            "consistency": consistency,
            "risk": risk,
            "score": score
        }
