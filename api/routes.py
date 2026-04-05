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
    webbrowser.open("http://127.0.0.1:8001/docs")

@app.on_event("startup")
def startup_event():
    logger.info("Starting up... opening browser dashboard")
    threading.Thread(target=open_browser).start()

# --- Pydantic Models for Structured Intelligence ---

class TraderMetrics(BaseModel):
    roi: Optional[float] = Field(None, description="Return on Investment (percentage)")
    win_rate: Optional[float] = Field(None, description="Percentage of successful trades")
    consistency: Optional[float] = Field(None, description="Score 0-1 representing trade frequency and success stability")
    risk_score: Optional[float] = Field(None, description="Score 0-1 representing volatility and exposure")

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

def safe_json_parse(text: str):
    """Clean LLM output and parse JSON."""
    raw = text.strip()
    if raw.startswith("```json"):
        raw = raw.replace("```json", "", 1)
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    return json.loads(raw.strip())

@app.post("/recommend-trader", response_model=IntelligenceReport, tags=["Intelligence"])
def recommend_trader(query: UserQuery):
    """
    Returns a structured intelligence report with a ranked list of top 3 traders.
    """
    try:
        logger.info(f"Intelligence Request: {query.prompt}")
        raw_response = decision_agent.recommend(query.prompt)
        
        # 1. Safe Parse
        data = safe_json_parse(raw_response)
        logger.info(f"[API] Parsed LLM Data: {data}")
        
        # 2. Sanitize metrics (Fix: Input should be a valid dictionary)
        if "top_traders" in data and isinstance(data["top_traders"], list):
            for trader in data["top_traders"]:
                if isinstance(trader, dict):
                    # If metrics is a list or not a dict, reset it to empty dict
                    if "metrics" in trader and not isinstance(trader["metrics"], dict):
                        logger.warning(f"Fixing invalid metrics type ({type(trader['metrics'])}) for {trader.get('username')}")
                        trader["metrics"] = {} 
                    # If metrics is missing, add empty dict (better for Pydantic)
                    if "metrics" not in trader:
                        trader["metrics"] = {}
        
        logger.info(f"[API] Final Sanitized Data: {data}")
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
    uvicorn.run(app, host="0.0.0.0", port=8001)
