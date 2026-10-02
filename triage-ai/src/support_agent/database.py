import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/support_agent.db")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customer_memories (
                memory_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                source TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                expires_at TEXT
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_customer_memories_customer_id
            ON customer_memories(customer_id)
            """
        )

        connection.commit()