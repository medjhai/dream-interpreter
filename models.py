from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from textblob import TextBlob
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Dream(Base):
    __tablename__ = 'dreams'
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    mood = Column(String(50))
    style = Column(String(20))
    interpretation = Column(Text)
    sentiment_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    feedbacks = relationship("Feedback", back_populates="dream")
    
    def analyze_sentiment(self):
        """Analyze the sentiment of the dream text"""
        analysis = TextBlob(self.text)
        self.sentiment_score = analysis.sentiment.polarity
        return self.sentiment_score

class Feedback(Base):
    __tablename__ = 'feedbacks'
    
    id = Column(Integer, primary_key=True)
    dream_id = Column(Integer, ForeignKey('dreams.id'))
    rating = Column(Integer)  # 1-5 stars
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    dream = relationship("Dream", back_populates="feedbacks")

# Database setup
def init_db():
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dreams.db')
    
    # Heroku Postgres fix
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    return Session()