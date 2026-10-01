from src.ingestion.cleaning import DocumentCleaner
from src.ingestion.context import CleanedDocument, ParsedDocument
from src.ingestion.stages.base import PipelineStage


class CleanStage(PipelineStage[ParsedDocument, CleanedDocument]):
    """Clean parsed document content."""

    def __init__(self, cleaner: DocumentCleaner) -> None:
        self.cleaner = cleaner

    def execute(
        self,
        data: ParsedDocument,
    ) -> CleanedDocument:
        return self.cleaner.clean(data)
