from sqlmodel import Session, create_engine

from api_service.core.config import settings

# Create database session that each class can use
database_engine = create_engine(settings.mssql_dsn.create_dsn(), 
                                connect_args={"checks_same_thread": False})

def get_mssql_connection():
    """
    Create SQL Server Database Session
    """
    session = Session(database_engine)
    try:
        yield session
    except Exception: # Might be good to name all the sessions
        session.rollback()
        raise
    finally:
        session.close()
