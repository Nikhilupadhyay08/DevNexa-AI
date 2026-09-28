import httpx
from typing import Protocol


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:3b"


class LLMProvider(Protocol):
    def generate(
        self,
        prompt: str,
    ) -> str:
        ...


class OllamaProvider:
    def __init__(
        self,
        model: str = OLLAMA_MODEL,
    ):
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:
        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty"
            )

        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]


class LLMService:
    def __init__(
        self,
        provider: LLMProvider,
    ):
        self.provider = provider

    def generate(
        self,
        prompt: str,
    ) -> str:
        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty"
            )

        return self.provider.generate(prompt)