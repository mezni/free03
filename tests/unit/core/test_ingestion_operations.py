from src.core.enums import DocumentProcessingOperation


def test_document_processing_operations():
    assert DocumentProcessingOperation.ADD.value == "add"
    assert DocumentProcessingOperation.UPDATE.value == "update"
    assert DocumentProcessingOperation.DELETE.value == "delete"
    assert DocumentProcessingOperation.SKIP.value == "skip"
    assert DocumentProcessingOperation.REINDEX.value == "reindex"
