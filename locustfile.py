"""Locust load-test scenario for the ticket-triage API.

Simulates a support-ticket submitter creating a case and requesting
classification. It uses the existing API and the fake classifier, so it does
not make paid LLM calls and never approves cases or triggers routing.

Authentication: set LOAD_TEST_TOKEN to a bearer token that the API's
TRIAGE_API_TOKENS registry recognizes with the "submitter" role.
"""

import os
import uuid

from locust import HttpUser, between, task


class SubmitterUser(HttpUser):
    """Create a case, then request classification for it."""

    wait_time = between(1, 3)

    def on_start(self) -> None:
        token = os.environ.get("LOAD_TEST_TOKEN", "")
        self.headers = {"Authorization": f"Bearer {token}"}

    @task
    def create_and_classify(self) -> None:
        unique = uuid.uuid4().hex
        case_id = f"LOAD-{unique}"
        payload = {
            "case_id": case_id,
            "ticket_id": f"T-{unique}",
            "subject": "Charged twice",
            "description": "I was charged twice for one order.",
        }

        with self.client.post(
            "/cases",
            json=payload,
            headers=self.headers,
            catch_response=True,
            name="/cases",
        ) as response:
            if response.status_code != 201:
                response.failure(f"create_case returned {response.status_code}")
                return

        with self.client.post(
            f"/cases/{case_id}/classify",
            headers=self.headers,
            catch_response=True,
            name="/cases/[id]/classify",
        ) as response:
            if response.status_code != 200:
                response.failure(f"classify returned {response.status_code}")
            elif response.json().get("status") != "pending_approval":
                response.failure("case did not reach pending_approval")
