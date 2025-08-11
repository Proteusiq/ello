from functools import partial

from litellm import acompletion

LLM_MODEL_NAME: str = "ollama/qwen3:latest"
chat = partial(
    acompletion,
    model=LLM_MODEL_NAME,
    api_base="http://localhost:11434",
    stream=True,
    top_p=0.9,
    temperature=0.2,
)
