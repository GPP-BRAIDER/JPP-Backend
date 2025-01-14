from app.database.db import engine, Base  # Ensure the correct import

def init_db() -> None:
    Base.metadata.create_all(bind=engine)