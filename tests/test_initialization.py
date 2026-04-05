import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory import PersistentMemory
from core.skill_manager import SkillManager
from agents.polymarket_agent import PolymarketAgent

def test_initialization():
    memory = PersistentMemory(db_path="data/test_memory.db")
    skill_manager = SkillManager(skills_dir="test_skills")
    
    poly_agent = PolymarketAgent(memory, skill_manager)
    print("PolymarketAgent initialized successfully.")
    
    assert poly_agent.name == "PolymarketAgent"
    print("Initialization test passed.")

if __name__ == "__main__":
    test_initialization()
