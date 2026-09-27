from typing import Protocol


class EmbeddingProvider(Protocol):
    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        ...


class EmbeddingService:
    def __init__(
        self,
        provider: EmbeddingProvider,
    ):
        self.provider = provider

    async def embed_chunk(
        self,
        text: str,
    ) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot create an embedding for empty text"
            )

        return await self.provider.embed_text(text)