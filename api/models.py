import uuid
import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass

# Conversation 1개 <-> Message N개 (1:N) 관계
class Conversation(Base):
    __tablename__ = "conversation"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), # 서버(mysql)가 직접 현재 시간으로 저장
    )
    

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True,
    )
    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversation.id")
    )
    role: Mapped[str] = mapped_column(String(10)) # user/assistant
    content: Mapped[str] = mapped_column(Text) # Text: 길이 제한 없는 문자열
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), # 서버(mysql)가 직접 현재 시간으로 저장
    )