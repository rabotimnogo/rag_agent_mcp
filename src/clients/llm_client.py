import os

from dotenv import load_dotenv

from openai import AsyncOpenAI
from .config import AgentConfig

load_dotenv()


class LLMClient:
    """
    Vibecode жесткий
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = AsyncOpenAI(api_key=config.api_key)

    async def complete(self, messages: list[dict], tools: list[dict] | None = None):
        return await self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            messages=messages,
            tools=tools or [],
            tool_choice="auto" if tools else "none",
        )
