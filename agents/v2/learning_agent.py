from core.base_agent import BaseAgent
from loguru import logger

class LearningAgent(BaseAgent):
    def __init__(self, memory=None, skill_manager=None, kb=None):
        system_prompt = """
        You are the Learning & Feedback Agent. You track predictions made by traders and agents, 
        and compare them against actual market outcomes to update reliability scores.
        """
        super().__init__("LearningAgent", system_prompt, memory, skill_manager)
        self.kb = kb

    def verify_outcome(self, trader_wallet, prediction, actual_outcome):
        """
        Closed Learning Loop: Update trader scores based on accuracy.
        """
        logger.info(f"[LearningAgent] Verifying outcome for {trader_wallet}: Prediction={prediction}, Actual={actual_outcome}")
        
        success = (prediction == actual_outcome)
        
        # Simple Feedback Logic
        if self.kb:
            # In a real system, you'd fetch the trader, update consistency/roi, and re-embed.
            # Here we reflect on the logic.
            reflection = f"""
            Trader {trader_wallet} was {'correct' if success else 'incorrect'}. 
            Prediction was {prediction} while actual was {actual_outcome}.
            Adjusting reliability metrics.
            """
            logger.info(reflection)
            
            # Hermes Reflection Feature: Learn from the mistake or success
            self.learn("Outcome Verification", reflection)
        
        return success
