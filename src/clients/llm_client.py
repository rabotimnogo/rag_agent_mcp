from dotenv import load_dotenv

from openai import OpenAI
from src.agent.config import AgentConfig

load_dotenv()


class LLMClient:
    """
    Vibecode жесткий
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key, base_url="https://openrouter.ai/api/v1"
        )

    async def complete(self, messages: list[dict], tools: list[dict] | None = None):
        return await self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            messages=messages,
            tools=tools or [],
            tool_choice="auto" if tools else "none",
        )
