from abc import ABC, abstractmethod


class PipelineStage[InputT, OutputT](ABC):
    """Base interface for an ingestion pipeline stage."""

    @abstractmethod
    def execute(self, data: InputT) -> OutputT:
        """Execute the pipeline stage."""
        raise NotImplementedError
