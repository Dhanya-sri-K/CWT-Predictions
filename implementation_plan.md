# Prediction Market Research Tool Implementation Plan

This project implements a multi-agent system to search and research prediction markets (Polymarket, Kalshi), identifying top traders, mapping them to niches, and enriching the data with RAG-based context.

## User Review Required

> [!IMPORTANT]
> This project requires **Apify API Token** and **OpenRouter API Key**.
> The "Closed Learning Loop" is implemented via a `SkillManager` that persists successful agent strategies as Markdown files, which are reloaded in subsequent runs.

## Proposed Changes

### Core Framework
Implement a lightweight agent framework inspired by Hermes Agent.

#### [NEW] [base_agent.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/core/base_agent.py)
Base class for all agents. Handles LLM communication via OpenRouter and tool execution.

#### [NEW] [skill_manager.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/core/skill_manager.py)
Implements the "Closed Learning Loop". Saves agent successes as "skills" (markdown) and loads them as context.

#### [NEW] [memory.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/core/memory.py)
SQLite-based persistent memory for conversation history and agent state.

---

### Specialized Agents

#### [NEW] [polymarket_agent.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/agents/polymarket_agent.py)
Uses Apify `saswave/polymarket-leaderboard-scraper` to find top-performing wallets.

#### [NEW] [kalshi_agent.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/agents/kalshi_agent.py)
Uses Apify `kalshi-market-scraper` to identify active markets and high-volume traders (where available).

#### [NEW] [niche_mapper_agent.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/agents/niche_mapper_agent.py)
Categorizes discovered traders into niches (NBA, Politics, Weather, etc.) based on their trade history.

#### [NEW] [research_agent.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/agents/research_agent.py)
Enriches RAG by searching for real-world context on specific events using Apify `apify/google-search-scraper`.

---

### Application Entry

#### [NEW] [main.py](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/main.py)
CLI interface for chatting with the agents and triggering searches.

#### [NEW] [.env](file:///c:/Users/DhanyaSri/Downloads/CWT%20predictions/.env)
Configuration for API keys.

---

## Verification Plan

### Automated Tests
- `pytest tests/test_core.py`: Tests `BaseAgent` and `SkillManager`.
- `pytest tests/test_apify.py`: Tests Apify integration (mocked).

### Manual Verification
1. Run `python main.py`.
2. Input: "Search for top Polymarket traders in the NBA niche".
3. Verify that the Polymarket agent triggers the Apify scraper.
4. Verify that the Niche Mapper categorizes the results.
5. Verify that a "skill" is generated in the `skills/` directory after a successful run.
6. Toggle the "research" mode to see the Research Agent enrich the output with Google Search data.
