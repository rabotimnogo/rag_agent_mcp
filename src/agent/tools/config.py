import os
from dotenv import load_dotenv
from pydantic import BaseModel
from src.constants.model_names.models_name import MODEL_NAME
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()


class AgentConfig(BaseModel):
    api_key: str
    model: str
    temperature: float
    top_p: float
    top_k: float
    system_prompt: str
    max_iterations: int = 10


config = AgentConfig(
    api_key=os.getenv("API_KEY_ROUTER"),
    model=MODEL_NAME,
    temperature=0.5,
    top_p=0.9,
    top_k=20,
    system_prompt=SYSTEM_PROMPT,
)
