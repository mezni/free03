from ticket_triage.errors import RoutingLookupInconclusiveError


class FakeLLMClient:
    def __init__(self, response: str) -> None:
        self.response = response
        self.last_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


class FakeRoutingProvider:
    """In-memory routing provider for tests.

    It can simulate a provider that accepts an operation but loses the response
    (``accept_then_timeout``), one whose lookup is inconclusive under eventual
    consistency (``mark_inconclusive``), and one that guarantees safe retries
    (``supports_safe_retry``).
    """

    def __init__(self, *, supports_safe_retry: bool = False) -> None:
        self.supports_safe_retry = supports_safe_retry
        self.confirmed: dict[str, str] = {}
        self.inconclusive: set[str] = set()
        self._route_errors: dict[str, BaseException] = {}
        self._accept_before_error: set[str] = set()
        self.route_calls: list[str] = []
        self.lookup_calls: list[str] = []

    def _reference(self, idempotency_key: str) -> str:
        return f"ext-{idempotency_key[:12]}"

    def route(self, *, ticket_id: str, destination: str, idempotency_key: str) -> str:
        self.route_calls.append(idempotency_key)
        error = self._route_errors.pop(idempotency_key, None)
        if error is not None:
            if idempotency_key in self._accept_before_error:
                self._accept_before_error.discard(idempotency_key)
                self.confirmed[idempotency_key] = self._reference(idempotency_key)
            raise error
        reference = self._reference(idempotency_key)
        self.confirmed[idempotency_key] = reference
        return reference

    def lookup_by_idempotency_key(self, idempotency_key: str) -> str | None:
        self.lookup_calls.append(idempotency_key)
        if idempotency_key in self.inconclusive:
            raise RoutingLookupInconclusiveError(
                "The provider cannot determine the outcome."
            )
        return self.confirmed.get(idempotency_key)

    def accept_then_timeout(self, idempotency_key: str) -> None:
        """Commit the operation, then lose the response."""
        self._accept_before_error.add(idempotency_key)
        self._route_errors[idempotency_key] = TimeoutError("provider timed out")

    def fail_route(self, idempotency_key: str, error: BaseException) -> None:
        self._route_errors[idempotency_key] = error

    def mark_inconclusive(self, idempotency_key: str) -> None:
        self.inconclusive.add(idempotency_key)
