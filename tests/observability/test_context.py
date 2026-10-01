from src.observability.context import (
    create_request_id,
    get_request_id,
    set_request_id,
)


class TestRequestId:
    def test_request_id(self) -> None:
        request_id = create_request_id()

        assert request_id
        assert get_request_id() == request_id

    def test_set_request_id(self) -> None:
        set_request_id("test-request")

        assert get_request_id() == "test-request"

    def test_default_is_none(self) -> None:
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                ("from src.observability.context import get_request_id; print(get_request_id())"),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.stdout.strip() == "None"

    def test_ids_are_unique(self) -> None:
        first = create_request_id()
        second = create_request_id()

        assert first != second

    def test_ids_are_valid_uuids(self) -> None:
        from uuid import UUID

        request_id = create_request_id()

        assert str(UUID(request_id)) == request_id
