from pathlib import Path


SYSTEM_PROMPT = Path("src/constants/prompts/system_prompt.md").read_text(
    encoding="utf-8"
)
