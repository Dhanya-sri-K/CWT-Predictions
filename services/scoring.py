import numpy as np

class ScoringService:
    @staticmethod
    def calculate_trader_score(roi, consistency, niche_accuracy, risk):
        """
        TraderScore = (0.4 * ROI) + (0.3 * Consistency) + (0.2 * Niche Accuracy) - (0.1 * Risk)
        Weights are normalized for demonstration.
        """
        # Ensure values are within reasonable bounds or normalized [0, 1]
        score = (0.4 * roi) + (0.3 * consistency) + (0.2 * niche_accuracy) - (0.1 * risk)
        return round(score, 4)

    @staticmethod
    def calculate_sharpe_ratio(returns):
        """
        Simplified risk-adjusted return metric.
        """
        if not returns or len(returns) < 2:
            return 0.0
        avg_return = np.mean(returns)
        std_dev = np.std(returns)
        return avg_return / std_dev if std_dev != 0 else avg_return
