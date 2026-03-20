import os

from src.clients.llm_client import LLMClient

from src.agent.config import config
from src.agent.memory import ChatMemory
from src.agent.tools.registry import ToolRegistry
from agent.tools.rag_tool import WeatherTool
from src.agent.runner import AgentRunner

from src.constants.model_names.models_name import MODEL_NAME
from prompts.system_prompt import SYSTEM_PROMPT


from src.agent.config import config


class Worker:
    def __init__(self):
        registry = ToolRegistry()
        registry.register(WeatherTool())
        memory = ChatMemory(system_prompt=config.system_prompt)
        llm = LLMClient(config=config)
        self.runner = AgentRunner(
            config=config, memory=memory, llm_client=llm, tools=registry
        )

    async def chat(self):
        end_dialogue = {"пошел нахуй", "exit", "пока", "завершить", "иди нахуй"}
        print("Агент готов. Для выхода введите 'exit'.\n")

        while True:
            user_input = input("Вы: ").strip()
            if not user_input:
                continue
            if user_input.lower() in end_dialogue:
                break
            response = await self.runner.run(user_input)
            print(f"Агент: {response}\n")

    async def run(self):
        await self.chat()
