import uuid
from costs.domain import organisation as o


def test_organisation_model_init():
    org_id = str(uuid.uuid4())
    org = o.Organisation(
        org_id=org_id,
        name="Aurora Innovations",
        currency="USD"
    )
    assert org.org_id == org_id
    assert org.name == "Aurora Innovations"
    assert org.currency == "USD"
    assert org.created_at == None
    assert org.updated_at == None
    assert org.deleted_at == None
