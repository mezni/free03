# Changelog

All notable changes to this project will be documented in this file.

## Version History

| Version | Feature Domain      | Key Objectives                                                            |
| ------- | ------------------- | ------------------------------------------------------------------------ |
| 0.1.4   | LLM Integration | `ChatOpenRouter` client factory wired to settings; new `llm` package     |
| 0.1.3   | CLI: Ticket Listing | `triage-ai tickets` command rendering seed tickets from the JSON loader |
| 0.1.2   | Data Ingestion      | JSON ticket loader with Pydantic validation into `SupportTicket` objects |
| 0.1.1   | Domain Models       | Pydantic `SupportTicket` model with validation, unit tests               |
| 0.1.0   | Project Foundations | Scaffold layout, pydantic-settings config, Typer CLI, pytest suite        |

## Unreleased

Next release will be **0.1.14**; subsequent releases increment the patch version (0.1.15, 0.1.16, ...).

## 0.1.13 - 2026-09-28

### Added

- `data/memory_behavior_cases.json` with 3 behavioral evaluation cases
- `src/support_agent/memory_behavior_evaluation.py` with `evaluate_memory_behavior()` function and LLM-based behavior judgment
- `src/support_agent/models.py` with `BehavioralEvaluation` Pydantic model for validated evaluation results
- `src/support_agent/run_memory_behavior_evaluation.py` CLI for running behavioral evaluation suite

### Fixed

- N/A

## 0.1.12 - 2026-09-28

### Added

- `src/support_agent/memory_service.py` with `MemoryService` class including `process_message()`, `retrieve()`, `get_context()`, `get_customer_memories()`, `delete()`, and `remove_expired()` methods
- `src/support_agent/prompts.py` with `build_triage_system_prompt()` function for building system prompts with optional memory context
- `src/support_agent/agent.py` with updated `SupportAgent` class supporting optional `MemoryService` integration and customer ID-based memory context
- `src/support_agent/memory_expiration.py` with `remove_expired_memories()` function
- `tests/test_agent_memory.py` with 4 tests for MemoryService functionality and prompt construction with memory context

### Fixed

- N/A

## 0.1.8 - 2026-09-28

### Added

- `src/support_agent/models.py` with `MemoryType` enum and updated `CustomerMemory` and `MemoryCandidate` models
- `src/support_agent/memory_expiration.py` with `calculate_expiration()` function and expiration policies per memory type
- `src/support_agent/memory_retrieval.py` with `retrieve_relevant_memories()` and `format_retrieved_memories()` functions
- `src/support_agent/memory_policy.py` with `ALLOWED_MEMORY_TYPES` and updated `should_store_memory()` to validate memory types
- `src/support_agent/customer_memory.py` with expiration-aware `get_customer_memories()`, and `MemoryType` parameter in `add_or_update_memory()`
- `src/support_agent/memory_manager.py` passes `memory_type` to `add_or_update_memory()` and calculates `expires_at`
- `tests/test_memory_retrieval.py` with 2 tests for memory retrieval and customer isolation
- `tests/test_memory.py` with 4 new tests: `test_higher_priority_source_wins`, `test_higher_confidence_same_source_wins`, `test_expired_memory_is_not_retrieved`, and `test_non_expiring_memory_is_retrieved`

### Fixed

- N/A

## 0.1.7 - 2026-09-28

### Added

- `src/support_agent/models.py` with `MemoryType` enum and updated `CustomerMemory` and `MemoryCandidate` models
- `src/support_agent/memory_expiration.py` with `calculate_expiration()` function and expiration policies per memory type
- `src/support_agent/memory_retrieval.py` with `retrieve_relevant_memories()` and `format_retrieved_memories()` functions
- `src/support_agent/memory_policy.py` with `ALLOWED_MEMORY_TYPES` and updated `should_store_memory()` to validate memory types
- `src/support_agent/customer_memory.py` with expiration-aware `get_customer_memories()`, and `MemoryType` parameter in `add_or_update_memory()`
- `src/support_agent/memory_manager.py` passes `memory_type` to `add_or_update_memory()` and calculates `expires_at`
- `tests/test_memory_retrieval.py` with 2 tests for memory retrieval and customer isolation
- `tests/test_memory.py` with 4 new tests: `test_higher_priority_source_wins`, `test_higher_confidence_same_source_wins`, `test_expired_memory_is_not_retrieved`, and `test_non_expiring_memory_is_retrieved`

### Fixed

- N/A

## 0.1.6 - 2026-09-28

### Added

- `src/support_agent/models.py` with `RetrievedMemory` model and `MemorySource` enum
- `src/support_agent/memory_retrieval.py` with `retrieve_relevant_memories()` and `format_retrieved_memories()` functions
- `src/support_agent/memory_policy.py` with `SOURCE_PRIORITY`, `MemoryDecision`, and `resolve_memory_conflict()` functions
- `tests/test_memory_retrieval.py` with 2 tests for memory retrieval and customer isolation
- `tests/test_memory.py` with 2 new tests: `test_higher_priority_source_wins` and `test_higher_confidence_same_source_wins`

### Fixed

- N/A

## 0.1.5 - 2026-09-28

### Added

- `src/support_agent/models.py` with `RetrievedMemory` model and `MemorySource` enum
- `src/support_agent/memory_retrieval.py` with `retrieve_relevant_memories()` and `format_retrieved_memories()` functions
- `src/support_agent/memory_policy.py` with `SOURCE_PRIORITY`, `MemoryDecision`, and `resolve_memory_conflict()` functions
- `tests/test_memory_retrieval.py` with 2 tests for memory retrieval and customer isolation
- `tests/test_memory.py` with 2 new tests: `test_higher_priority_source_wins` and `test_higher_confidence_same_source_wins`

### Fixed

- N/A

## 0.1.5 - 2026-09-28

### Added

- `src/support_agent/memory.py` with `ConversationMemory` dataclass for managing conversation history
- `src/support_agent/agent.py` with `SupportAgent` class integrating memory with LLM calls and tool use
- `src/support_agent/state.py` with `AgentState` dataclass and `update_state_from_extraction()` function
- `src/support_agent/models.py` with `ExtractedTicket`, `CustomerMemory`, `MemoryCandidate`, and `MemoryExtractionResult` models
- `src/support_agent/prompts.py` with `MEMORY_EXTRACTION_SYSTEM_PROMPT`
- `src/support_agent/customer_memory.py` with in-memory customer memory store (`add_or_update_memory()`, `get_customer_memories()`, `delete_memory()`)
- `src/support_agent/memory_extraction.py` with `extract_memory_candidates()` function for LLM-based memory extraction
- `src/support_agent/memory_policy.py` with `should_store_memory()` policy function and constants (`MIN_MEMORY_CONFIDENCE`, `ALLOWED_MEMORY_KEYS`)
- `src/support_agent/memory_manager.py` with `process_message_for_memory()` to connect extraction, policy, and storage
- `tests/test_memory.py` with 8 tests covering user messages, conversation history, clear memory, state extraction, memory creation, duplicate handling, value updates, and memory deletion
- `tests/test_memory_extraction.py` with 3 tests for `MemoryCandidate` and `MemoryExtractionResult` models
- `tests/test_memory_policy.py` with 5 tests for `should_store_memory()` policy validation
- `tests/test_memory_manager.py` with 2 integration tests connecting extraction → policy → storage (using monkeypatched LLM)

### Fixed

- `update_state_from_extraction()` now handles both enum and string values for category and priority fields

## 0.1.2 - 2026-09-24

### Added

- `src/triage_ai/data` package with `loader.py` exposing `load_tickets()`.
- `load_tickets()` reads a JSON array and validates each entry into a `SupportTicket` model.

## 0.1.1 - 2026-09-24

### Added

- `SupportTicket` Pydantic model (`ticket_id`, `customer_id`, `subject`, `description`) with field validation.
- `tests/test_ticket.py` covering model creation and validation errors.

## 0.1.0 - 2026-09-24

### Added

- Project scaffold: `src/triage_ai`, `tests`, `data`, `prompts`, `docs` layout.
- Dependency management via `uv` (`pyproject.toml`, `uv.lock`).
- Configuration layer with `pydantic-settings` (`Settings` model, `.env` support).
- Typer CLI with `info` command and Rich output.
- CLI entry point `triage-ai` registered in `pyproject.toml`.
- `pytest` test suite covering configuration defaults.
- `.env.example` and `.gitignore` for local development.