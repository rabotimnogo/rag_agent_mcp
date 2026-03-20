import json
from src.clients.llm_client import LLMClient
from src.agent.memory import BaseMemory
from src.agent.tools.config import AgentConfig, config
from src.agent.tools.registry import ToolRegistry


class AgentRunner:
    def __init__(
        self,
        config: AgentConfig,
        memory: BaseMemory,
        llm_client: LLMClient,
        tools: ToolRegistry,  # переименовал tool_registry -> tools
    ):
        self.config = config
        self.memory = memory
        self.llm = llm_client
        self.tools = tools

    async def run(self, user_input: str) -> str:
        self.memory.add("user", user_input)

        for _ in range(self.config.max_iterations):
            response = await self.llm.complete(
                messages=self.memory.get_messages(),
                tools=self.tools.get_schemas(),
            )
            message = response.choices[0].message
            tool_calls = message.tool_calls

            if not tool_calls:
                return message.content

            # добавляем сообщение от LLM с tool_calls в память
            self.memory.messages.append(message)

            for tc in tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                result = self.tools.execute(tc.function.name, args)
                self.memory.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tc.function.name,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        raise RuntimeError("Max iterations reached")
