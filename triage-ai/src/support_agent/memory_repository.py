from datetime import datetime, timezone

from support_agent.database import get_connection, initialize_database
from support_agent.models import (
    CustomerMemory,
    MemorySource,
    MemoryType,
)


# Initialize the database table when the module is imported
initialize_database()

class MemoryRepository:

    def save(
        self,
        memory: CustomerMemory,
    ) -> None:

        with get_connection() as connection:

            connection.execute(
                """
                INSERT OR REPLACE INTO customer_memories (
                    memory_id,
                    customer_id,
                    key,
                    value,
                    memory_type,
                    source,
                    confidence,
                    created_at,
                    updated_at,
                    expires_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    memory.memory_id,
                    memory.customer_id,
                    memory.key,
                    memory.value,
                    memory.memory_type.value,
                    memory.source.value,
                    memory.confidence,
                    memory.created_at.isoformat(),
                    memory.updated_at.isoformat(),
                    (
                        memory.expires_at.isoformat()
                        if memory.expires_at
                        else None
                    ),
                ),
            )

            connection.commit()

    def get_by_customer(
        self,
        customer_id: str,
    ) -> list[CustomerMemory]:

        with get_connection() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM customer_memories
                WHERE customer_id = ?
                """,
                (customer_id,),
            ).fetchall()

        return [
            self._row_to_memory(row)
            for row in rows
        ]

    def delete(
        self,
        memory_id: str,
    ) -> bool:

        with get_connection() as connection:

            cursor = connection.execute(
                """
                DELETE FROM customer_memories
                WHERE memory_id = ?
                """,
                (memory_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

    @staticmethod
    def _row_to_memory(
        row: object,
    ) -> CustomerMemory:

        expires_at = (
            datetime.fromisoformat(row["expires_at"])
            if row["expires_at"]
            else None
        )

        return CustomerMemory(
            memory_id=row["memory_id"],
            customer_id=row["customer_id"],
            key=row["key"],
            value=row["value"],
            memory_type=MemoryType(row["memory_type"]),
            source=MemorySource(row["source"]),
            confidence=row["confidence"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            expires_at=expires_at,
        )