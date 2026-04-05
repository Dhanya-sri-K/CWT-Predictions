import random
from loguru import logger

class BacktestService:
    def __init__(self):
        pass

    def run_simulation(self, wallet: str, days: int = 30):
        """
        Simulates following a trader's activity over X days.
        In a real system, this would query historical trade data from the DB.
        """
        logger.info(f"[BacktestService] Running simulation for {wallet} over {days} days")
        
        # Deterministic-ish random based on wallet string for demo consistency
        seed = sum(ord(c) for c in wallet)
        random.seed(seed)
        
        pnl = random.uniform(5, 25)
        win_rate = random.uniform(0.55, 0.85)
        max_drawdown = random.uniform(2, 8)
        
        return {
            "wallet": wallet,
            "period_days": days,
            "simulated_pnl_percent": round(pnl, 2),
            "max_drawdown": round(max_drawdown, 2),
            "win_probability": round(win_rate, 2),
            "trades_simulated": random.randint(15, 100),
            "confidence_interval": "95%"
        }
