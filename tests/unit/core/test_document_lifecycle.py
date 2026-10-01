from src.core.enums import DocumentLifecycleStatus


def test_document_lifecycle_status_values():
    assert DocumentLifecycleStatus.PENDING.value == "pending"
    assert DocumentLifecycleStatus.PROCESSING.value == "processing"
    assert DocumentLifecycleStatus.ACTIVE.value == "active"
    assert DocumentLifecycleStatus.FAILED.value == "failed"
    assert DocumentLifecycleStatus.DELETED.value == "deleted"
