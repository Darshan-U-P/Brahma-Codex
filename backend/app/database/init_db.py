from app.database.base import Base
from app.database.session import engine

# Import all models so SQLAlchemy knows about them.
from app.models import Project  # noqa: F401


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)