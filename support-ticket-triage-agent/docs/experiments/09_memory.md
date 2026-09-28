# Experiment 09 — Conversation Memory

## Goal

Understand how an agent maintains conversation state across
multiple interactions.

## Initial behavior

The agent created a new message history for every execution.

Previous conversation context was lost after the function returned.

## Implementation

Added:

- `ConversationMemory` in `src/support_agent/memory/conversation.py`
- persistent message list for a conversation
- memory injection into `run_agent()` via optional parameter
- user message storage via `add_user_message()`
- assistant message storage via `add_assistant_message()`
- tool result storage via `add_message("user", tool_results)`

## Key design

The agent does not own memory lifetime — the caller creates and
passes `ConversationMemory`, enabling:

- **Shared context**: multiple `run_agent()` calls can share the
  same memory, preserving conversation history
- **Fresh start**: passing a new `ConversationMemory()` starts a
  fresh conversation
- **Single source of truth**: `memory.get_messages()` is the source
  of truth for `chat_with_tools()`, not a separate local list

## Important distinction

- **Working memory**: state required during a single agent execution
  (tool budgets, iteration counters)
- **Conversation memory**: persists interaction history across
  `run_agent()` calls, injected by the caller

## Current limitations

- No persistence across application restarts
- No summarization or context-window management
- No long-term customer memory
- No memory retrieval / summarization policies
- Tool results can increase context size linearly

## Future improvements

- persistent conversation storage (JSON/sqlite)
- conversation summaries/abstraction
- memory retrieval / selection of relevant history
- context window limits and trimming
- customer history / profile integration
- memory policies (what to keep/discard)