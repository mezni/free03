from dotenv import load_dotenv

from ticket_triage.api import create_app
from ticket_triage.application import TriageApplicationService
from ticket_triage.classification import FakeClassifier
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.sqlite_repository import SQLiteCaseRepository

load_dotenv()

repository = SQLiteCaseRepository("ticket_triage.db")
service = TriageApplicationService(repository)

# Use the fake classifier during local development.
# Replace it with the real LLMClassifier + OpenAILLMClient
# when you are ready to make real model requests.
classifier = FakeClassifier()

policy = RecommendationPolicy(
    allowed_categories={"billing", "account", "general"},
    allowed_destinations={
        "billing-team",
        "account-support",
        "general-support",
    },
)

app = create_app(
    service=service,
    classifier=classifier,
    policy=policy,
)