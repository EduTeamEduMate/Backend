from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship("User")
    questions = relationship("Question", back_populates="exam")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey('exams.id'))
    question_text = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    false_answer_1 = Column(String, nullable=False)
    false_answer_2 = Column(String, nullable=False)
    false_answer_3 = Column(String, nullable=False)

    # Relationships
    exam = relationship("Exam", back_populates="questions")