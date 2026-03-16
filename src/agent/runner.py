import json

from src.clients.llm_client import LLMClient
from src.agent.memory import BaseMemory
from src.agent.config import AgentConfig
from src.agent.tools.registry import ToolRegistry


class AgentRunner:
    """
    Главный оркестратор агентного цикла.
    Единственное место, где живёт логика loop:
      1. Отправить сообщения + тулы в LLM
      2. Если LLM хочет вызвать тул — вызвать через Registry
      3. Добавить результат в Memory, повторить
      4. Если нет tool_call — вернуть финальный ответ

    max_iterations — защита от бесконечного цикла (обязательно!).
    Позже сюда можно добавить:
      - planning step (ReAct / CoT)
      - параллельный вызов нескольких тулов
      - A2A (вызов другого агента как тула)
    """

    def __init__(
        self,
        config: AgentConfig,
        memory: BaseMemory,
        llm_client: LLMClient,
        tool_registry: ToolRegistry,
    ):
        self.config = config
        self.memory = memory
        self.llm = llm_client
        self.tools = tool_registry

    def run(self, user_input: str) -> str:
        self.memory.add("user", user_input)

        for _ in range(self.config.max_iterations):
            response = self.llm.complete(
                messages=self.memory.get_messages(),
                tools=self.tools.get_schemas(),
            )

            message = response.choices[0].message
            tool_calls = message.tool_calls

            if not tool_calls:
                # Финальный ответ — выходим из цикла
                return message.content

            # Обрабатываем все tool_calls (LLM может запросить несколько сразу)
            self.memory.add_raw(message)  # сырое сообщение от LLM
            for tc in tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                result = self.tools.execute(tc.function.name, args)
                self.memory.add_tool_result(tc.id, tc.function.name, result)

        raise RuntimeError("Max iterations reached")
