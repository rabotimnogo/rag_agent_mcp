from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any


class BaseTool(ABC):
    """
    Абстрактный базовый класс для всех тулов.
    Каждый тул ОБЯЗАН реализовать:
      - name: str — идентификатор, который видит LLM
      - description: str — что умеет тул
      - args_schema: BaseModel — Pydantic-схема аргументов
      - execute(**kwargs) — сама логика

    Такая структура позволит позже:
      - добавить MCP-тулы, просто реализовав этот интерфейс
      - автогенерировать JSON schema для API из args_schema
      - добавить retry-логику / логирование в базовый execute()
    """

    name: str
    description: str
    args_schema: type[BaseModel]

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

    def to_openai_schema(self) -> dict:
        """Автоматически генерирует schema для OpenAI tools из Pydantic модели."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.args_schema.model_json_schema(),
            },
        }
