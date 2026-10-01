# ADR-003: Index Versioning

## Decision

Maintain explicit index versions with BUILDING, ACTIVE, RETIRED and FAILED states.

## Reason

Reindexing should be isolated from the currently serving index.

A new index must be validated before activation.