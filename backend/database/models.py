"""
Database models for the Campus Q&A Agent.
Uses SQLAlchemy ORM with SQLite (development) / MySQL (production).
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid

Base = declarative_base()

def generate_uuid():
    """Generate a unique identifier for records."""
    return str(uuid.uuid4())

class Conversation(Base):
    """
    Represents a conversation session between user and the Q&A agent.
    A conversation contains multiple messages.
    """
    __tablename__ = 'conversations'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), nullable=False, index=True)  # Browser session identifier
    user_id = Column(String(36), nullable=True, index=True)  # Optional user authentication
    title = Column(String(200), nullable=True)  # Auto-generated from first question
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation {self.id[:8]}... '{self.title}'>"

class Message(Base):
    """
    Represents a single message in a conversation.
    Can be from user (question) or assistant (answer).
    """
    __tablename__ = 'messages'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey('conversations.id'), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)  # The message text
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # For assistant messages only
    source_documents = Column(Text, nullable=True)  # JSON array of source document IDs
    confidence_score = Column(Float, nullable=True)  # Confidence of the answer (0.0-1.0)
    processing_time_ms = Column(Integer, nullable=True)  # Time taken to generate answer
    model_used = Column(String(50), nullable=True)  # Which LLM model was used

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    feedback = relationship("Feedback", back_populates="message", uselist=False)

    def __repr__(self):
        role_emoji = {'user': '👤', 'assistant': '🤖', 'system': '⚙️'}
        return f"<Message {role_emoji.get(self.role, '?')} {self.id[:8]}...>"

class Feedback(Base):
    """
    User feedback on assistant answers.
    Helps improve the RAG system over time.
    """
    __tablename__ = 'feedback'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey('messages.id'), nullable=False, unique=True, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    helpful = Column(Boolean, nullable=True)  # Was the answer helpful?
    correct = Column(Boolean, nullable=True)  # Was the answer factually correct?
    comments = Column(Text, nullable=True)  # Free-text feedback
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    message = relationship("Message", back_populates="feedback")

    def __repr__(self):
        return f"<Feedback {self.rating}⭐ for message {self.message_id[:8]}...>"

class QAPair(Base):
    """
    Question-Answer pairs from the knowledge base.
    Used for training, evaluation, and as reference data.
    """
    __tablename__ = 'qa_pairs'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question = Column(Text, nullable=False, index=True)
    answer = Column(Text, nullable=False)
    source = Column(String(200), nullable=True)  # Source website/document
    category = Column(String(50), nullable=True, index=True)  # e.g., 'library', 'dormitory', 'academic'
    tags = Column(String(200), nullable=True)  # Comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Embedding vector (stored separately in FAISS, but we keep metadata here)
    embedding_id = Column(String(50), nullable=True, index=True)  # ID in vector store

    def __repr__(self):
        return f"<QAPair '{self.question[:50]}...'>"

class SystemMetrics(Base):
    """
    System performance and usage metrics.
    For monitoring and optimization.
    """
    __tablename__ = 'system_metrics'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    metric_type = Column(String(50), nullable=False, index=True)  # e.g., 'response_time', 'cache_hit_rate'
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    details = Column(Text, nullable=True)  # JSON details about the metric

    def __repr__(self):
        return f"<SystemMetrics {self.metric_type}: {self.value} at {self.timestamp}>"