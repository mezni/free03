# Data Flow

## Ingestion

Filesystem
→ Source
→ Change Detector
→ Loader
→ Parser
→ Cleaner
→ Metadata Extractor
→ Chunker
→ Embedding Provider
→ Indexing Service
→ PostgreSQL/pgvector

## Retrieval

Query
→ Query Analyzer
→ Retrieval Pipeline
→ Search Strategy
→ PostgreSQL/pgvector
→ Candidate Results
→ Reranker
→ Context Selector

## Generation

Query + Context
→ Prompt Builder
→ LLM Provider
→ Generated Answer
→ Citation Extractor
→ Grounding Validation
→ RAG Response

## Evaluation

Evaluation Dataset
→ Retrieval/RAG Runner
→ Metrics
→ Quality Gate
→ CI/CD