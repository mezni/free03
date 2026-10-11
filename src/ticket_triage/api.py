from fastapi import FastAPI, HTTPException, status

from ticket_triage.api_schemas import (
    CaseResponse,
    CreateCaseRequest,
    RecommendationResponse,
)
from ticket_triage.application import (
    ApplicationError,
    TriageApplicationService,
)
from ticket_triage.classification import Classifier
from ticket_triage.domain import CaseStatus, Ticket
from ticket_triage.policy import RecommendationPolicy


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

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/cases",
        status_code=status.HTTP_201_CREATED,
        response_model=CaseResponse,
    )
    def create_case(request: CreateCaseRequest) -> CaseResponse:
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
    def get_case(case_id: str) -> CaseResponse:
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
    def classify(case_id: str) -> CaseResponse:
        try:
            case = service.get_case(case_id)
            if case.status == CaseStatus.RECEIVED:
                case = service.start_processing(case_id)
            if case.status == CaseStatus.PENDING_APPROVAL:
                return to_case_response(case)
            case = service.classify_case(
                case_id,
                classifier=classifier,
                policy=policy,
            )
        except ApplicationError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            )
        return to_case_response(case)

    return app