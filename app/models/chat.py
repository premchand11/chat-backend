import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    universe = Column(String, nullable=False)
    total_messages = Column(Integer, default=0)
    time_span_days = Column(Integer, default=0)
