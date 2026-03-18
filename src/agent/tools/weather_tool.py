from pydantic import BaseModel
from .base import BaseTool


class WeatherArgs(BaseModel):
    city: str


class WeatherTool(BaseTool):
    """
    Конкретный тул — минимум кода благодаря BaseTool.
    Вся бизнес-логика только в execute().
    Добавить новый тул = создать новый файл по этому шаблону.
    """

    name = "get_weather"
    description = "Получить погоду в городе"
    args_schema = WeatherArgs

    def execute(self, city: str) -> str:
        return f"В {city} сейчас 19°C"
