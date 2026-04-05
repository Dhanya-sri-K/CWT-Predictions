import os
import json
from loguru import logger

class SkillManager:
    def __init__(self, skills_dir="skills"):
        self.skills_dir = skills_dir
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)

    def save_skill(self, agent_name, task, strategy):
        filename = f"{agent_name}_{task.replace(' ', '_').lower()}.md"
        filepath = os.path.join(self.skills_dir, filename)
        
        content = f"# Skill: {task}\n\n**Agent**: {agent_name}\n\n## Successful Strategy\n{strategy}\n"
        
        with open(filepath, "w") as f:
            f.write(content)
        logger.info(f"Skill saved to {filepath}")

    def get_relevant_skills(self, query):
        """
        Simple keyword-based skill retrieval.
        """
        relevant_skills = []
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".md"):
                # Simple check: if a word from query is in the filename
                keywords = query.lower().split()
                if any(kw in filename.lower() for kw in keywords if len(kw) > 3):
                    with open(os.path.join(self.skills_dir, filename), "r") as f:
                        relevant_skills.append(f.read())
        return relevant_skills
