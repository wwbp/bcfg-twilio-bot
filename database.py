import logging
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(module)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- Database Setup ---
SQLALCHEMY_DATABASE_URL = 'sqlite:///./chat.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}  # SQLite specific
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Models ---


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    # Relationship to chat transcripts
    transcripts = relationship("ChatTranscript", back_populates="user")


class ChatTranscript(Base):
    __tablename__ = 'chat_transcripts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)  # e.g., 'user' or 'assistant'
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="transcripts")


# Create the tables in the database (for demo purposes; use Alembic for production)
Base.metadata.create_all(bind=engine)

# --- Functions for Chat Operations ---


def verify_update_database(id: str, message):
    """
    Verify if the participant (or group) exists in the database;
    create a new record if not.
    """
    logger.info(f"Checking database for participant/group ID: {id}")
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if user:
        logger.info(f"Participant/group ID {id} exists.")
    else:
        logger.warning(
            f"Participant/group ID {id} not found. Creating a new record. Received message: {message}"
        )
        user = User(id=id)
        db.add(user)
        db.commit()
    db.close()


def load_chat_history_json(id: str):
    """
    Load chat history from the database for the given participant/group ID.
    Returns a list of dictionaries representing each chat message.
    """
    logger.info(f"Loading chat history for participant/group ID: {id}")
    db = SessionLocal()
    transcripts = (
        db.query(ChatTranscript)
        .filter(ChatTranscript.user_id == id)
        .order_by(ChatTranscript.created_at.asc())
        .all()
    )
    db.close()
    history = [
        {
            "role": transcript.role,
            "content": transcript.content,
        }
        for transcript in transcripts
    ]
    return history


def save_chat_round(id: str, message, response):
    """
    Save a chat round to the database by storing both the user's message and the assistant's response.
    """
    logger.info(f"Saving chat round for participant/group ID: {id}")
    db = SessionLocal()

    # Ensure the user exists
    user = db.query(User).filter(User.id == id).first()
    if not user:
        user = User(id=id)
        db.add(user)
        db.commit()

    # Create and add the user's message
    user_message = ChatTranscript(
        user_id=id,
        role='user',
        content=message
    )
    db.add(user_message)

    # Create and add the assistant's response
    assistant_message = ChatTranscript(
        user_id=id,
        role='assistant',
        content=response
    )
    db.add(assistant_message)

    db.commit()
    db.close()
    logger.info("Chat round saved successfully.")
