from pydantic import BaseModel


class AgentConfig(BaseModel):
    api_key: str
    model: str
    temperature: float
    top_p: float
    top_k: float
    system_prompt: str
    max_iterations: int = 10  # защита от бесконечного цикла
