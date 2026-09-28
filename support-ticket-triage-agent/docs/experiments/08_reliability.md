# Experiment 08 — Reliability

## Goal

Observe how the agent behaves when tools fail.

## Failure cases

- Unknown tool
- Tool exception
- Invalid tool arguments
- Repeated tool calls
- Agent exceeding iteration limit

## Initial behavior

The original dispatcher allowed tool exceptions to propagate
directly into the agent loop.

This caused the agent application to terminate.

## Reliability changes

Added:

- ToolExecutionResult
- Dispatcher error boundary
- Structured tool errors
- Maximum agent iterations
- Maximum tool-call budget
- Explicit model instructions for failed tools

## Important observation

Read-only tools and state-changing tools should not automatically
have the same retry policy.

Retrying a read operation is generally safer than retrying an
operation that creates persistent state.

## Future improvements

- Exponential backoff
- Timeouts
- Idempotency keys
- Structured logging
- Tracing
- Circuit breakers
- More specific exception types