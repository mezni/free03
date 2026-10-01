from pathlib import Path

from src.ingestion.sources.filesystem import FilesystemSource
from src.ingestion.stages.discover import DiscoveryStage


def test_discovery_stage(tmp_path: Path):
    document = tmp_path / "policy.md"

    document.write_text(
        "# Policy\n\nTest policy.",
        encoding="utf-8",
    )

    source = FilesystemSource(tmp_path)
    stage = DiscoveryStage(source)

    documents = stage.execute()

    assert len(documents) == 1
    assert documents[0].path == document
