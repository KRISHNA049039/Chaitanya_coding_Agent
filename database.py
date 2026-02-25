"""
PostgreSQL Database Integration
Stores conversation history, user preferences, and context
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from typing import Optional, List, Dict, Any

# Database URL from environment or default to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///kiro_agent.db"  # SQLite fallback for easy setup
)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Models
class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    context_items = relationship("ContextStore", back_populates="user")


class Session(Base):
    """Chat session model"""
    __tablename__ = "sessions"
    
    id = Column(String(255), primary_key=True)  # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    session_metadata = Column(JSON, default={})  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), ForeignKey("sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    tool_calls = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="messages")


class ContextStore(Base):
    """Context storage for user-specific information"""
    __tablename__ = "context_store"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="context_items")


# Database operations
class DatabaseManager:
    """Manager for database operations"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def init_db(self):
        """Initialize database tables"""
        Base.metadata.create_all(bind=self.engine)
        print("✓ Database initialized")
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    # User operations
    def create_user(self, username: str, email: Optional[str] = None, preferences: Optional[Dict] = None) -> User:
        """Create a new user"""
        db = self.get_session()
        try:
            user = User(
                username=username,
                email=email,
                preferences=preferences or {}
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        db = self.get_session()
        try:
            return db.query(User).filter(User.id == user_id).first()
        finally:
            db.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        db = self.get_session()
        try:
            return db.query(User).filter(User.username == username).first()
        finally:
            db.close()
    
    # Session operations
    def create_session(self, session_id: str, user_id: Optional[int] = None, metadata: Optional[Dict] = None) -> Session:
        """Create a new session"""
        db = self.get_session()
        try:
            session = Session(
                id=session_id,
                user_id=user_id,
                session_metadata=metadata or {}  # Updated to use session_metadata
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session
        finally:
            db.close()
    
    def get_session_obj(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        db = self.get_session()
        try:
            return db.query(Session).filter(Session.id == session_id).first()
        finally:
            db.close()
    
    def update_session_activity(self, session_id: str):
        """Update session last_active timestamp"""
        db = self.get_session()
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if session:
                session.last_active = datetime.utcnow()
                db.commit()
        finally:
            db.close()
    
    # Message operations
    def add_message(self, session_id: str, role: str, content: str, tokens_used: int = 0, tool_calls: Optional[List] = None) -> Message:
        """Add a message to a session"""
        db = self.get_session()
        try:
            message = Message(
                session_id=session_id,
                role=role,
                content=content,
                tokens_used=tokens_used,
                tool_calls=tool_calls or []
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            
            # Update session activity
            self.update_session_activity(session_id)
            
            return message
        finally:
            db.close()
    
    def get_session_messages(self, session_id: str, limit: Optional[int] = None) -> List[Message]:
        """Get messages for a session"""
        db = self.get_session()
        try:
            query = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at)
            if limit:
                query = query.limit(limit)
            return query.all()
        finally:
            db.close()
    
    def get_recent_messages(self, session_id: str, limit: int = 10) -> List[Message]:
        """Get recent messages for a session"""
        db = self.get_session()
        try:
            return db.query(Message).filter(
                Message.session_id == session_id
            ).order_by(Message.created_at.desc()).limit(limit).all()[::-1]  # Reverse to chronological
        finally:
            db.close()
    
    # Context operations
    def set_context(self, user_id: int, key: str, value: Any):
        """Set context value for user"""
        db = self.get_session()
        try:
            context = db.query(ContextStore).filter(
                ContextStore.user_id == user_id,
                ContextStore.key == key
            ).first()
            
            if context:
                context.value = value
                context.updated_at = datetime.utcnow()
            else:
                context = ContextStore(
                    user_id=user_id,
                    key=key,
                    value=value
                )
                db.add(context)
            
            db.commit()
        finally:
            db.close()
    
    def get_context(self, user_id: int, key: str) -> Optional[Any]:
        """Get context value for user"""
        db = self.get_session()
        try:
            context = db.query(ContextStore).filter(
                ContextStore.user_id == user_id,
                ContextStore.key == key
            ).first()
            return context.value if context else None
        finally:
            db.close()
    
    def get_all_context(self, user_id: int) -> Dict[str, Any]:
        """Get all context for user"""
        db = self.get_session()
        try:
            contexts = db.query(ContextStore).filter(ContextStore.user_id == user_id).all()
            return {ctx.key: ctx.value for ctx in contexts}
        finally:
            db.close()
    
    # Analytics
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get statistics for a user"""
        db = self.get_session()
        try:
            sessions = db.query(Session).filter(Session.user_id == user_id).all()
            total_messages = sum(len(s.messages) for s in sessions)
            
            return {
                "total_sessions": len(sessions),
                "total_messages": total_messages,
                "first_session": min(s.started_at for s in sessions) if sessions else None,
                "last_active": max(s.last_active for s in sessions) if sessions else None
            }
        finally:
            db.close()


# Global instance
db_manager = DatabaseManager()


# Initialize database on import
def init_database():
    """Initialize database tables"""
    try:
        db_manager.init_db()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        print("Using in-memory storage instead")


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print("Database setup complete!")
