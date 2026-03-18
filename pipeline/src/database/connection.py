import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL


def get_engine():
    """Create SQLAlchemy engine."""
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db():
    """Initialize database schema."""
    engine = get_engine()

    # Path relativo ao arquivo connection.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "schema.sql")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()

    print("   ✅ Database schema initialized")
    return engine


def get_session(engine):
    """Create a database session."""
    Session = sessionmaker(bind=engine)
    return Session()