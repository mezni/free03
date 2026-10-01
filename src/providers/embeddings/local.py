import hashlib
import math

from src.embeddings.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    """Small deterministic embedding provider for development and tests."""

    def __init__(self, dimensions: int = 8) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions must be greater than zero")

        self._dimensions = dimensions

    @property
    def model_name(self) -> str:
        return "local-deterministic"

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def _embed_text(self, text: str) -> list[float]:
        values: list[float] = []

        for index in range(self._dimensions):
            digest = hashlib.sha256(
                f"{index}:{text}".encode("utf-8")
            ).digest()

            integer = int.from_bytes(digest[:4], byteorder="big")

            values.append((integer / 2**32) * 2 - 1)

        magnitude = math.sqrt(
            sum(value * value for value in values)
        )

        if magnitude == 0:
            return values

        return [value / magnitude for value in values]