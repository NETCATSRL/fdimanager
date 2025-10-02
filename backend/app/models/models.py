from datetime import datetime
from sqlalchemy import BigInteger, Column, Integer, String, Text, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db.session import Base
import enum

class UserLevel(enum.IntEnum):
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4

class UserStatus(str, enum.Enum):
    active = "active"
    pending = "pending"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)
    level = Column(Integer, nullable=False, default=1)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.active)
    approved_by = Column(Integer, nullable=True)
    approved_at = Column(DateTime)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    contents_authored = relationship("Content", back_populates="author")

class Content(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    link = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    author = relationship("User", back_populates="contents_authored")
    visibility = relationship("ContentVisibility", back_populates="content", cascade="all, delete-orphan")

class ContentVisibility(Base):
    __tablename__ = "content_visibility"
    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    level_target = Column(Integer, nullable=True)

    content = relationship("Content", back_populates="visibility")

    __table_args__ = (
        UniqueConstraint('content_id', 'user_id', name='ux_visibility_user'),
        UniqueConstraint('content_id', 'level_target', name='ux_visibility_level'),
    )
