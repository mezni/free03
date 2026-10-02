from support_agent.memory_service import MemoryService


class FakeMemoryService:

    def __init__(self):
        self.processed_messages = []

    def process_message(self, message):
        self.processed_messages.append(message)
        return []

    def get_context(
        self,
        customer_id,
        query,
        limit=5,
    ):
        return "- preferred_contact_method: email"


def test_memory_service_has_get_context():
    service = MemoryService()
    assert hasattr(service, "get_context")


def test_fake_memory_service():
    fake = FakeMemoryService()
    result = fake.process_message("Hello")
    assert len(fake.processed_messages) == 1
    context = fake.get_context("C001", "test query")
    assert "- preferred_contact_method: email" in context


from support_agent.prompts import build_triage_system_prompt


def test_memory_is_added_to_prompt():

    prompt = build_triage_system_prompt(
        memory_context="- preferred_contact_method: email"
    )

    assert "preferred_contact_method" in prompt
    assert "email" in prompt


def test_prompt_without_memory():

    prompt = build_triage_system_prompt()

    assert "Relevant customer memory:" not in prompt
