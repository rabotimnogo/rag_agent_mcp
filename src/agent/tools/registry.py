from .base import BaseTool
from typing import Dict, List


class ToolRegistry:
    """
    Хранит все тулы, умеет их искать и вызывать по имени.
    AgentRunner знает только про Registry — не про конкретные тулы.
    Это развязывает зависимости: добавляешь тул → регистрируешь → готово.

    В будущем сюда можно добавить:
      - динамическую загрузку MCP-тулов
      - фильтрацию тулов по контексту (Agentic RAG)
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get_schemas(self) -> List[dict]:
        """Отдаёт список schemas для передачи в LLM API."""
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def execute(self, name: str, args: dict):
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")
        return self._tools[name].execute(**args)
