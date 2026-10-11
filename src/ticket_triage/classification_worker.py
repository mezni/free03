"""Worker handler that executes queued classification jobs.

Classification is intentionally isolated from human approval and routing. A
successful job leaves the case in ``pending_approval``; it never approves a
recommendation or routes a ticket.

Delivery is at-least-once, so the handler is written to be idempotent: if a
previous attempt already produced a recommendation awaiting approval, a retry
returns immediately instead of classifying again.
"""

from ticket_triage.domain import CaseStatus
from ticket_triage.job_queue import Job


def handle_classification_job(
    job: Job,
    *,
    service,
    classifier,
    policy,
) -> None:
    if job.job_type != "classify_ticket":
        raise ValueError(f"Unsupported job type: {job.job_type}")

    case_id = job.payload.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("Job payload must contain a case_id.")

    case = service.get_case(case_id)

    # A previous attempt may have completed classification before crashing
    # between the workflow update and recording job success.
    if case.status == CaseStatus.PENDING_APPROVAL:
        return

    if case.status == CaseStatus.RECEIVED:
        service.start_processing(case_id)
        case = service.get_case(case_id)

    if case.status != CaseStatus.PROCESSING:
        raise ValueError(
            f"Case {case_id} cannot be classified from status {case.status.value}."
        )

    service.classify_case(
        case_id,
        classifier=classifier,
        policy=policy,
    )
