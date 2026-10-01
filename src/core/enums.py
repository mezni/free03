from enum import StrEnum


class DocumentChangeType(StrEnum):
    """Change detected for a source document."""

    NEW = "new"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


class DocumentLifecycleStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    ACTIVE = "active"
    FAILED = "failed"
    DELETED = "deleted"


class IndexOperation(StrEnum):
    """Supported index operations."""

    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    REINDEX = "reindex"


class IndexVersionStatus(StrEnum):
    BUILDING = "building"
    ACTIVE = "active"
    RETIRED = "retired"
    FAILED = "failed"


class IngestionRunStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class IngestionJobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DocumentProcessingStatus(StrEnum):
    SUCCESS = "success"
    SKIPPED = "skipped"
    FAILED = "failed"


class DocumentProcessingOperation(StrEnum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    SKIP = "skip"
    REINDEX = "reindex"
