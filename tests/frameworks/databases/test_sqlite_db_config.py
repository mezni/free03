from src.frameworks.databases.sqlite_db_config import DBConnectionHandler

def test_create_sqlite_db_engine():
    db_connection_handle = DBConnectionHandler()
    engine = db_connection_handle.get_engine()

    assert engine is not None