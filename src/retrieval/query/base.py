from abc import ABC, abstractmethod

from src.models.query_analysis import QueryAnalysis


class QueryAnalyzer(ABC):
    """Turns a raw user query into a structured QueryAnalysis."""

    @abstractmethod
    def analyze(self, query: str) -> QueryAnalysis:
        raise NotImplementedError