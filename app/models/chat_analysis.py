from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ChatAnalysis(Base):

    __tablename__ = "chat_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    universe = Column(String(50), nullable=False)
    participants_count = Column(Integer)
    analysis = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
