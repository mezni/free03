import time
from hashlib import sha256
from typing import Any

from src.models.retrieval import RetrievalFilter


def _filters_to_repr(filters: RetrievalFilter | None) -> str:
    """Hash a RetrievalFilter into a canonical string for use in a cache key."""
    if filters is None:
        return "none"
    parts = []
    if filters.source is not None:
        parts.append(f"source={filters.source}")
    if filters.document_id is not None:
        parts.append(f"doc_id={filters.document_id}")
    if filters.document_type is not None:
        parts.append(f"doc_type={filters.document_type}")
    parts.sort()
    return "|".join(parts)


def make_cache_key(
    query: str,
    top_k: int,
    candidate_k: int | None,
    filters: RetrievalFilter | None,
    index_version_id: Any,
    knowledge_base_id: UUID,
) -> str:
    """Build a deterministic cache key for retrieval results.

    The key encodes all parameters that affect the retrieval outcome so
    that changing any one of them produces a distinct key, and in
    particular that changing `index_version_id` alone changes the key.

    The key is a short string suitable as a dictionary key or memcached
    entry name.
    """
    # Deterministic hash components
    qhash = sha256(query.encode()).hexdigest()[:12]

    kpart = f"k={top_k}"

    cpart = f"ck={candidate_k}" if candidate_k is not None else "ck=None"

    # Filters canonical form
    fpart = _filters_to_repr(filters)

    # Index version ID as hex string
    vid = str(index_version_id) if index_version_id is not None else "None"

    # Knowledge base ID for isolation boundary
    kb_id = str(knowledge_base_id)

    return ":".join([qhash, kpart, cpart, fpart, vid, kb_id])


class RetrievalCache:
    """In-memory cache for retrieval results.

    A single process / worker. A horizontally scaled deployment needs a
    shared store (e.g. Redis) with a key space that mirrors this
    construction.

    The cache stores full retrieval results so that an identical query
    (same parameters) does not need to re-run the pipeline.  When the
    index version changes, the key changes automatically, so the new
    results are fetched from the DB.
    """

    def __init__(self, max_size: int = 500) -> None:
        self._max_size = max_size
        self._store: dict[str, tuple[float, Any]] = {}  # key → (ttl_epoch, result)

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None

        ttl_epoch, result = entry
        if ttl_epoch is not None and ttl_epoch < time.time():
            # Expired
            del self._store[key]
            return None

        return result

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        if len(self._store) >= self._max_size and key not in self._store:
            # Simple eviction: drop the oldest entry
            oldest = min(self._store, key=lambda k: self._store[k][0])
            del self._store[oldest]

        entry = (time.time() + (ttl_seconds or 300), value)
        self._store[key] = entry

    def invalidate_by_index_version(self, old_index_version_id: Any) -> None:
        """Remove cache entries that were keyed on a retired index version.

        This is an inexpensive way to purge stale results without a full
        flush.  In a production deployment a shared cache would have a
        version tag or namespace; here we just delete matching keys.
        """
        to_delete = [
            key
            for key in self._store
            if f":{str(old_index_version_id)}" in key
        ]
        for key in to_delete:
            del self._store[key]