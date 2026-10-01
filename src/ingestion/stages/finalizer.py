import shutil
from pathlib import Path


class FileFinalizer:
    def __init__(
        self,
        processed_dir: Path,
        archive_flag: bool = True,
    ) -> None:
        self.processed_dir = processed_dir
        self.archive_flag = archive_flag

    def finalize(self, source_path: Path) -> None:
        if not source_path.exists():
            return

        if self.archive_flag:
            self._archive(source_path)
        else:
            source_path.unlink()

    def _archive(self, source_path: Path) -> None:
        self.processed_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = self.processed_dir / source_path.name

        if destination.exists():
            destination = self._unique_destination(destination)

        shutil.move(
            str(source_path),
            str(destination),
        )

    @staticmethod
    def _unique_destination(path: Path) -> Path:
        counter = 1

        while True:
            candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")

            if not candidate.exists():
                return candidate

            counter += 1
