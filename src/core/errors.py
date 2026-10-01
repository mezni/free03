from __future__ import annotations


class AetherError(Exception):
    """Base exception for Aether RAG."""


class ConfigError(AetherError):
    """Configuration-related errors."""


class NotFoundError(AetherError):
    """Requested resource not found."""
