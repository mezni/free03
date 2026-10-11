"""Deterministic keys that identify intended external side effects.

The key must be stable across retries so that a request that was already sent
is recognized as the same intended effect. Generating a fresh random key on
retry would defeat that purpose and allow duplicate assignments.
"""

import hashlib


def routing_idempotency_key(
    case_id: str,
    recommendation_version: int,
) -> str:
    """Return the stable idempotency key for routing a recommendation.

    Identical inputs always produce the same key. A new recommendation version
    for the same case produces a different key, because it is a different
    intended external effect. In a multi-tenant deployment the tenant
    identifier must be part of the operation identity as well.
    """
    if not case_id.strip():
        raise ValueError("case_id must not be empty")

    if recommendation_version < 1:
        raise ValueError("recommendation_version must be positive")

    identity = f"ticket-triage:routing:{case_id}:v{recommendation_version}"

    return hashlib.sha256(identity.encode("utf-8")).hexdigest()
