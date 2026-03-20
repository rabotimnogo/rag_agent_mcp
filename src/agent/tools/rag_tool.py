import pandas as pd

from pydantic import BaseModel
from .base import BaseTool


class ShemaRAG(BaseModel):
    query: str


class ToolRAG(BaseTool):
    """
    Конкретный тул — минимум кода благодаря BaseTool.
    Вся бизнес-логика только в execute().
    Добавить новый тул = создать новый файл по этому шаблону.
    """

    name = "rag_tool"
    description = "Cходить в RAG, получить какую-то хуйню"
    args_schema = ShemaRAG

    def execute(self, query: str) -> str:
        return ["Ты пидорас"]
