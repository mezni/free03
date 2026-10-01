from uuid import uuid4

from fastapi.testclient import TestClient

# Patch get_settings to return test configuration
import src.config.settings as _settings_mod
from src.api.app import create_app
from src.api.dependencies import get_document_service, get_ingestion_service
from src.core.enums import DocumentLifecycleStatus
from src.models.document import Document

_original_get_settings = _settings_mod.get_settings


def _patched_get_settings():
    """Return test configuration that bypasses API key auth issues."""
    from src.config.settings import ApplicationConfig, EnvironmentSettings, LoggingConfig, Settings

    return Settings(
        environment=EnvironmentSettings(
            database_url="postgresql://test:test@localhost/test",
            openrouter_api_key="test-key",
        ),
        application=ApplicationConfig(
            name="rag-system",
            environment="test",
        ),
        logging=LoggingConfig(level="INFO"),
        security={
            "api": {
                "enabled": True,
                "api_key_header": "X-API-Key",
            },
            "general": {
                "title": "rag-system",
            }
        },
        api_key="test-key",  # Set a test API key
    )


_settings_mod.get_settings = _patched_get_settings


class FakeDocumentService:
    def __init__(self):
        self._documents = {
            uuid4(): Document(
                id=uuid4(),
                source="filesystem",
                source_uri="/data/policy.md",
                title="Company Policy",
                document_type="markdown",
                content_hash="a" * 64,
                status=DocumentLifecycleStatus.ACTIVE,
                created_at=None,
                updated_at=None,
            )
        }

    def list_documents(self, source=None, status=None, limit=50, offset=0):
        items = list(self._documents.values())
        if source:
            items = [d for d in items if d.source == source]
        if status:
            items = [d for d in items if d.status.value == status]
        total = len(items)
        return items[offset:offset + limit], total

    def get_document(self, document_id):
        return self._documents.get(document_id)

    def delete_document(self, document_id):
        if document_id in self._documents:
            del self._documents[document_id]


class FakeIngestionService:
    def ingest(self):
        from uuid import uuid4

        return type("obj", (object,), {
            "run_id": str(uuid4()),
            "discovered_count": 3,
            "processed_count": 2,
            "skipped_count": 1,
            "failed_count": 0,
            "document_ids": [str(uuid4()) for _ in range(2)],
        })()


def _make_app():
    app = create_app()
    app.dependency_overrides[get_document_service] = lambda: FakeDocumentService()
    app.dependency_overrides[get_ingestion_service] = lambda: FakeIngestionService()
    return app


def test_list_documents_with_auth():
    """List documents with valid authentication returns 200."""
    app = _make_app()
    client = TestClient(app, headers={"X-API-Key": "test-key"})
    response = client.get("/documents")
    assert response.status_code == 200


def test_list_documents_without_auth():
    """List documents without API key returns 401."""
    app = _make_app()
    client = TestClient(app)
    response = client.get("/documents")
    assert response.status_code == 401


def test_get_document_found():
    """Retrieve an existing document by ID."""
    app = _make_app()
    client = TestClient(app, headers={"X-API-Key": "test-key"})
    # First list to get a document ID
    list_response = client.get("/documents", headers={"X-API-Key": "test-key"})
    assert list_response.status_code == 200
    doc_id = str(list_response.json()["items"][0]["id"])
    response = client.get(f"/documents/{doc_id}", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200


def test_get_document_not_found():
    """Retrieve a document that doesn't exist."""
    app = _make_app()
    client = TestClient(app, headers={"X-API-Key": "test-key"})
    fake_id = str(uuid4())
    response = client.get(f"/documents/{fake_id}", headers={"X-API-Key": "test-key"})
    assert response.status_code == 404


def test_delete_document_found():
    """Delete an existing document."""
    app = _make_app()
    client = TestClient(app, headers={"X-API-Key": "test-key"})
    # First list to get a document ID
    list_response = client.get("/documents", headers={"X-API-Key": "test-key"})
    assert list_response.status_code == 200
    doc_id = str(list_response.json()["items"][0]["id"])
    response = client.delete(f"/documents/{doc_id}", headers={"X-API-Key": "test-key"})
    assert response.status_code == 204


def test_delete_document_not_found():
    """Delete a document that doesn't exist."""
    app = _make_app()
    client = TestClient(app, headers={"X-API-Key": "test-key"})
    fake_id = str(uuid4())
    response = client.delete(f"/documents/{fake_id}", headers={"X-API-Key": "test-key"})
    assert response.status_code == 404


def test_ingest_documents():
    """Trigger document ingestion from a path."""
    app = _make_app()
    client = TestClient(app, headers={"X-API-Key": "test-key"})
    response = client.post(
        "/documents/ingest",
        json={"path": "data/raw/billing"},
        headers={"X-API-Key": "test-key"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert "discovered_count" in data
    assert "processed_count" in data
    assert "skipped_count" in data
    assert "failed_count" in data
    assert "document_ids" in data