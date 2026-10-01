from src.ingestion.context import ParsedDocument, RawDocument
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.stages.base import PipelineStage


class ParseStage(PipelineStage[RawDocument, ParsedDocument]):
    """Parse raw documents using the appropriate parser."""

    def __init__(self, registry: ParserRegistry) -> None:
        self.registry = registry

    def execute(
        self,
        data: RawDocument,
    ) -> ParsedDocument:
        parser = self.registry.get_parser(data.document.source_uri)

        return parser.parse(data)
