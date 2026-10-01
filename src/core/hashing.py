import hashlib
from pathlib import Path


def calculate_file_hash(path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
