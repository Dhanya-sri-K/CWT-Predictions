from fastapi import FastAPI, HTTPException, Query as FastAPIQuery
from pydantic import BaseModel, Field
from typing import List, Optional
from agents.v2.decision_agent import DecisionAgent
from agents.v2.analyzer_agent import AnalyzerAgent
from agents.polymarket_agent import PolymarketAgent
from services.backtest_service import BacktestService
from loguru import logger
import json
import webbrowser
import threading
import time

app = FastAPI(
    title="Prediction Market Intelligence Engine",
    description="Professional multi-agent system for trader discovery, performance analysis, and copy-trading advice.",
    version="2.0.0"
)

def open_browser():
    """Wait for server to start and then open the browser."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000/docs")

@app.on_event("startup")
def startup_event():
    logger.info("Starting up... opening browser dashboard")
    threading.Thread(target=open_browser).start()

# --- Pydantic Models for Structured Intelligence ---

class TraderMetrics(BaseModel):
    roi: float = Field(..., description="Return on Investment (percentage)")
    win_rate: float = Field(..., description="Percentage of successful trades")
    consistency: float = Field(..., description="Score 0-1 representing trade frequency and success stability")
    risk_score: float = Field(..., description="Score 0-1 representing volatility and exposure")

class TopTrader(BaseModel):
    wallet: str
    username: Optional[str] = None
    metrics: TraderMetrics
    explanation: str = Field(..., description="Why this trader was selected")

class IntelligenceReport(BaseModel):
    query: str
    confidence_score: float = Field(..., description="AI confidence in this recommendation (0-1)")
    top_traders: List[TopTrader]
    market_context: str = Field(..., description="Real-world context (news/sentiment) affecting this niche")
    recommendation_summary: str

class UserQuery(BaseModel):
    prompt: str = Field(..., example="Who is the best NBA trader for today's games?")

# --- API Endpoints ---

# Initialize Agents & Services
decision_agent = DecisionAgent()
poly_agent = PolymarketAgent()
backtest_service = BacktestService()

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to the Prediction Market Intelligence Engine v2"}

@app.post("/recommend-trader", response_model=IntelligenceReport, tags=["Intelligence"])
def recommend_trader(query: UserQuery):
    """
    Returns a structured intelligence report with a ranked list of top 3 traders, 
    detailed metrics, and market context.
    """
    try:
        logger.info(f"Intelligence Request: {query.prompt}")
        # This will now return a JSON string from DecisionAgent
        raw_response = decision_agent.recommend(query.prompt)
        
        # Parse the JSON string into our model
        data = json.loads(raw_response)
        return data
    except Exception as e:
        logger.exception("Error in /recommend-trader")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top-traders", response_model=List[TopTrader], tags=["Discovery"])
def get_leaderboard():
    """
    Returns the current top 10 traders from the discovery agents.
    """
    try:
        summary, traders = poly_agent.discover_traders()
        # Transform to structured list (Mocking metrics for this endpoint)
        results = []
        for t in traders[:10]:
            results.append({
                "wallet": t.get("proxy", "unknown"),
                "username": t.get("username"),
                "metrics": {"roi": 15.5, "win_rate": 0.72, "consistency": 0.8, "risk_score": 0.2},
                "explanation": "High historical profit on Polymarket leaderboard."
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backtest", tags=["Analytics"])
def backtest_trader(wallet: str, days: int = 30):
    """
    Simulates performance if you had followed this trader for the last X days.
    """
    try:
        return backtest_service.run_simulation(wallet, days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
