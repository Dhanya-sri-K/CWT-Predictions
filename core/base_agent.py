import os
from loguru import logger
from utils.openrouter_client import OpenRouterClient

class BaseAgent:
    def __init__(self, name, system_prompt, memory=None, skill_manager=None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = OpenRouterClient()
        self.memory = memory
        self.skill_manager = skill_manager

    def run(self, user_input, context=None):
        logger.info(f"[{self.name}] Running for input: {user_input[:50]}...")
        
        # Load relevant skills if available
        skills_context = ""
        if self.skill_manager:
            skills = self.skill_manager.get_relevant_skills(user_input)
            if skills:
                skills_context = "\n\nRelevant Skills learned from previous tasks:\n" + "\n".join(skills)
        
        messages = [
            {"role": "system", "content": self.system_prompt + skills_context},
        ]
        
        # Add memory if available
        if self.memory:
            history = self.memory.get_history(self.name)
            messages.extend(history)
            
        messages.append({"role": "user", "content": user_input})
        
        # Execute LLM call
        response = self.llm.complete(messages)
        
        # Store in memory
        if self.memory:
            self.memory.add_message(self.name, "user", user_input)
            self.memory.add_message(self.name, "assistant", response)
            
        logger.info(f"[{self.name}] Response generated.")
        return response

    def learn(self, task, successful_strategy):
        """
        Closed Learning Loop: Save a successful strategy as a skill.
        """
        if self.skill_manager:
            self.skill_manager.save_skill(self.name, task, successful_strategy)
            logger.info(f"[{self.name}] New skill learned for task: {task}")
