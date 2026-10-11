import logging
import time
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status

from ticket_triage.api_schemas import (
    CaseResponse,
    CreateCaseRequest,
    DecisionRequest,
    RecommendationResponse,
)
from ticket_triage.application import (
    ApplicationError,
    TriageApplicationService,
)
from ticket_triage.auth import (
    Principal,
    get_current_principal,
    require_roles,
)
from ticket_triage.classification import Classifier
from ticket_triage.domain import CaseStatus, DecisionType, Ticket
from ticket_triage.logging_config import (
    correlation_id_var,
    valid_correlation_id,
)
from ticket_triage.metrics import (
    CLASSIFICATION_ATTEMPTS,
    CLASSIFICATION_DURATION,
    HTTP_REQUEST_DURATION,
    HTTP_REQUESTS,
    render_metrics,
)
from ticket_triage.policy import RecommendationPolicy

logger = logging.getLogger("ticket_triage.http")


def to_case_response(case) -> CaseResponse:
    recommendation = None
    if case.recommendation is not None:
        recommendation = RecommendationResponse(
            category=case.recommendation.category,
            priority=case.recommendation.priority,
            destination=case.recommendation.destination,
            rationale=case.recommendation.rationale,
        )
    return CaseResponse(
        case_id=case.case_id,
        ticket_id=case.ticket.ticket_id,
        status=case.status,
        recommendation=recommendation,
        recommendation_version=case.recommendation_version,
    )


def create_app(
    *,
    service: TriageApplicationService,
    classifier: Classifier,
    policy: RecommendationPolicy,
) -> FastAPI:
    app = FastAPI()

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        supplied_id = request.headers.get("X-Correlation-ID")
        correlation_id = (
            supplied_id if valid_correlation_id(supplied_id) else uuid.uuid4().hex
        )

        token = correlation_id_var.set(correlation_id)
        started = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        except Exception:
            logger.error(
                "http_request_failed",
                extra={
                    "event": "http_request_failed",
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                },
            )
            raise
        finally:
            duration_seconds = time.perf_counter() - started
            HTTP_REQUESTS.labels(
                method=request.method,
                status=str(status_code),
            ).inc()
            HTTP_REQUEST_DURATION.labels(method=request.method).observe(
                duration_seconds
            )
            duration_ms = round(duration_seconds * 1000, 2)
            logger.info(
                "http_request_completed",
                extra={
                    "event": "http_request_completed",
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
            )
            correlation_id_var.reset(token)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/live")
    def health_live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    def health_ready() -> dict[str, str]:
        if not service.health_check():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service is not ready.",
            )
        return {"status": "ok"}

    @app.get("/metrics")
    def metrics() -> Response:
        content, media_type = render_metrics()
        return Response(content=content, media_type=media_type)

    @app.post(
        "/cases",
        status_code=status.HTTP_201_CREATED,
        response_model=CaseResponse,
    )
    def create_case(
        request: CreateCaseRequest,
        principal: Principal = Depends(require_roles("submitter", "admin")),
    ) -> CaseResponse:
        ticket = Ticket(
            ticket_id=request.ticket_id,
            subject=request.subject,
            description=request.description,
        )
        try:
            case = service.create_case(
                case_id=request.case_id,
                ticket=ticket,
            )
        except ApplicationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )
        return to_case_response(case)

    @app.get(
        "/cases/{case_id}",
        response_model=CaseResponse,
    )
    def get_case(
        case_id: str,
        principal: Principal = Depends(get_current_principal),
    ) -> CaseResponse:
        try:
            case = service.get_case(case_id)
        except ApplicationError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            )
        return to_case_response(case)

    @app.post(
        "/cases/{case_id}/classify",
        response_model=CaseResponse,
    )
    def classify(
        case_id: str,
        principal: Principal = Depends(require_roles("submitter", "admin", "system")),
    ) -> CaseResponse:
        try:
            case = service.get_case(case_id)
            if case.status == CaseStatus.RECEIVED:
                case = service.start_processing(case_id)
            if case.status == CaseStatus.PENDING_APPROVAL:
                return to_case_response(case)
            started = time.perf_counter()
            try:
                case = service.classify_case(
                    case_id,
                    classifier=classifier,
                    policy=policy,
                )
            except ApplicationError:
                CLASSIFICATION_ATTEMPTS.labels(outcome="application_error").inc()
                raise
            except Exception:
                CLASSIFICATION_ATTEMPTS.labels(outcome="unexpected_error").inc()
                raise
            else:
                CLASSIFICATION_ATTEMPTS.labels(outcome="success").inc()
            finally:
                CLASSIFICATION_DURATION.observe(time.perf_counter() - started)
        except ApplicationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )
        return to_case_response(case)

    @app.post(
        "/cases/{case_id}/decision",
        response_model=CaseResponse,
    )
    def decide(
        case_id: str,
        request: DecisionRequest,
        principal: Principal = Depends(require_roles("reviewer", "admin")),
    ) -> CaseResponse:
        decision = (
            DecisionType.APPROVED
            if request.decision == "approve"
            else DecisionType.REJECTED
        )
        try:
            case = service.decide(
                case_id,
                decision_id=request.decision_id,
                actor_id=principal.subject,
                decision=decision,
                comment=request.comment,
            )
        except ApplicationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )
        return to_case_response(case)

    return app
