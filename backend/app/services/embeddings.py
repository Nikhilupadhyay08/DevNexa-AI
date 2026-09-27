from typing import Protocol

from sentence_transformers import SentenceTransformer


class EmbeddingProvider(Protocol):
    def embed_text(self, text: str) -> list[float]:
        ...


class LocalEmbeddingProvider:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot create an embedding for empty text"
            )

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()


class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def embed_chunk(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError(
                "Cannot create an embedding for empty text"
            )

        return self.provider.embed_text(text)