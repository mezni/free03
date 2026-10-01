from abc import ABC, abstractmethod

from src.models.generation import (
    GenerationRequest,
    GenerationResponse,
)


class LLMProvider(ABC):
    """Interface for generating answers from a prompt and context."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        raise NotImplementedError
