import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOMAIN_FILE = PROJECT_ROOT / "src" / "ticket_triage" / "domain.py"

FORBIDDEN_IMPORTS = {
    "fastapi",
    "sqlite3",
    "openai",
    "prometheus_client",
}


def test_domain_does_not_import_infrastructure():
    tree = ast.parse(DOMAIN_FILE.read_text(encoding="utf-8"))

    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module.split(".")[0])

    violations = imported_modules & FORBIDDEN_IMPORTS

    assert not violations, (
        f"Domain imports infrastructure modules: {sorted(violations)}"
    )
