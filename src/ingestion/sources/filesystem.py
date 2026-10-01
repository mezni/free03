from pathlib import Path

from src.ingestion.context import DocumentInput
from src.ingestion.sources.base import DocumentSource


class FilesystemSource(DocumentSource):
    """Discover documents from a filesystem directory."""

    def __init__(
        self,
        input_dir: str | Path,
        patterns: tuple[str, ...] = ("*.md", "*.txt", "*.pdf"),
    ) -> None:
        self.input_dir = Path(input_dir)
        self.patterns = patterns

    def discover(self) -> list[DocumentInput]:
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory does not exist: {self.input_dir}")

        documents: list[DocumentInput] = []

        for pattern in self.patterns:
            for path in self.input_dir.rglob(pattern):
                if not path.is_file():
                    continue

                documents.append(
                    DocumentInput(
                        source="filesystem",
                        source_uri=str(path),
                        path=path,
                    )
                )

        return sorted(
            documents,
            key=lambda document: str(document.path),
        )
