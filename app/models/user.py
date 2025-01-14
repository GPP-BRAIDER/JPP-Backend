from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from app.database.db import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    role = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)

    points = Column(Integer)

    country = Column(String)
    city = Column(String)
    address = Column(String)
    postal_code = Column(String)
    phone_number = Column(String)
