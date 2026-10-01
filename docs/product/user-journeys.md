# User Journeys

## Knowledge Administrator Journey

### Ingest a New Document

1. Place a new document file in the monitored directory
2. System discovers the new document via FilesystemSource
3. Change Detector marks document as NEW
4. Loader reads the raw content
5. Parser extracts structured content (Markdown/Text)
6. Cleaner normalizes the text
7. Metadata Extractor pulls metadata (title, source, tags)
8. Chunker splits content into chunks
9. Embedding Provider generates embeddings for each chunk
10. Indexing Service persists chunks and embeddings to PostgreSQL
11. Document status changes to ACTIVE
12. Administrator receives confirmation

### Reindex Knowledge Base

1. Initiate reindex from the admin interface
2. Versioning Service creates a BUILDING index
3. Reindex Service processes all discovered documents into the BUILDING index
4. Index Validation Service validates the BUILDING index:
   - Checks chunk/embedding counts
   - Verifies embedding dimensions
   - Detects duplicates
   - Ensures no missing embeddings
5. If validation passes, Indexing Service activates the new index
6. Previous ACTIVE index becomes RETIRED
7. Administrator can monitor reindex status

### Monitor Index Health

1. Check /health endpoint for liveness
2. Check /health/ready endpoint for database readiness
3. View ingestion run history in the database
4. Monitor document processing status (SUCCESS, SKIPPED, FAILED)
5. Receive alerts on FAILED reindex events

## Application Developer Journey

### Query the RAG API

1. Obtain an API key for authentication
2. POST to /rag/query with a question and optional top_k parameter
3. System queries the ACTIVE index
4. Retrieval pipeline returns ranked chunks
5. LLM generates an answer grounded in the retrieved context
6. Citation Extractor identifies supporting sources
7. Grounding Validation checks that the answer is supported
8. RAGResponse returned with answer, citations, and metadata

### Handle Errors

1. Invalid requests return validation errors (422)
2. Protected endpoints return 401/403 if authentication fails
3. Provider timeouts return error with request ID
4. Internal errors do not expose implementation details

### Monitor API Health

1. Regularly check /health for service liveness
2. Check /health/ready for database connectivity
3. Review error logs for unusual patterns
4. Track API usage metrics

## End User Journey

### Ask a Question

1. End user submits a question via the application UI
2. Application calls POST /rag/query with the question
3. System processes the question through the pipeline
4. Retrieved chunks are reranked and contextualized
5. LLM generates an answer using only the supplied sources
6. Answer is returned with citations to supporting documents
7. End user sees the answer with source references

### Receive Answer with Citations

1. Answer text is displayed to the user
2. Citations are shown as clickable references
3. Each citation includes document ID, chunk ID, and chunk index
4. User can click citations to view source context
5. If information is unsupported, the system indicates this rather than inventing an answer