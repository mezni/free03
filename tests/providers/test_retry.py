import pytest

from src.core.exceptions import (
    ProviderResponseError,
    ProviderTimeoutError,
    TransientProviderError,
)
from src.providers.retry import RetryPolicy


def policy(max_retries: int = 2) -> RetryPolicy:
    return RetryPolicy(
        max_retries=max_retries,
        delay_seconds=0,
    )


class TestRetryPolicy:
    def test_retry_eventually_succeeds(self):
        attempts = 0

        def operation():
            nonlocal attempts

            attempts += 1

            if attempts < 3:
                raise RuntimeError("temporary")

            return "success"

        p = RetryPolicy(max_retries=2, delay_seconds=0)

        assert p.execute(operation) == "success"
        assert attempts == 3

    def test_immediate_success_makes_one_attempt(self):
        calls = []

        assert policy().execute(
            lambda: calls.append(1) or "ok"
        ) == "ok"
        assert len(calls) == 1

    def test_raises_after_exhausting_retries(self):
        calls = []

        def operation():
            calls.append(1)

            raise TransientProviderError("still down")

        with pytest.raises(TransientProviderError):
            policy(max_retries=2).execute(operation)

        assert len(calls) == 3

    def test_zero_retries_means_one_attempt(self):
        calls = []

        def operation():
            calls.append(1)

            raise TransientProviderError("down")

        with pytest.raises(TransientProviderError):
            policy(max_retries=0).execute(operation)

        assert len(calls) == 1

    def test_timeout_is_retried(self):
        calls = []

        def operation():
            calls.append(1)

            if len(calls) < 2:
                raise ProviderTimeoutError("slow")

            return "recovered"

        assert policy().execute(operation) == "recovered"
        assert len(calls) == 2

    def test_client_error_is_not_retried(self):
        """A 4xx is deterministic: retrying only repeats the failure."""
        calls = []

        def operation():
            calls.append(1)

            raise ProviderResponseError("invalid api key")

        with pytest.raises(ProviderResponseError):
            policy(max_retries=3).execute(operation)

        assert len(calls) == 1

    def test_transient_error_is_retried_but_not_client_error(
        self,
    ):
        calls = []

        def operation():
            calls.append(1)

            raise TransientProviderError("server error")

        with pytest.raises(TransientProviderError):
            policy(max_retries=3).execute(operation)

        assert len(calls) == 4

    def test_unrelated_exception_is_not_retried(self):
        calls = []

        def operation():
            calls.append(1)

            raise RuntimeError("programming error")

        with pytest.raises(RuntimeError):
            policy(max_retries=3).execute(operation)

        assert len(calls) == 1

    def test_custom_retryable_set(self):
        calls = []

        def operation():
            calls.append(1)

            raise RuntimeError("custom")

        p = RetryPolicy(
            max_retries=2,
            delay_seconds=0,
            retryable_exceptions=(RuntimeError,),
        )

        with pytest.raises(RuntimeError):
            p.execute(operation)

        assert len(calls) == 3

    def test_default_retryable_set(self):
        from src.providers.retry import DEFAULT_RETRYABLE

        assert ProviderTimeoutError in DEFAULT_RETRYABLE
        assert TransientProviderError in DEFAULT_RETRYABLE
        assert ProviderResponseError not in DEFAULT_RETRYABLE