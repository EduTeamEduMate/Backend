from pydantic import BaseModel, EmailStr
from typing import List


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr

class LoginResponse(BaseModel):
    user: User
    token: str
    
class UserUpdate(BaseModel):
    name: str
    email: str
    
class QuestionBase(BaseModel):
    question_text: str
    correct_answer: str
    false_answer_1: str
    false_answer_2: str
    false_answer_3: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    class Config:
        orm_mode = True

class ExamBase(BaseModel):
    name: str

class ExamCreate(ExamBase):
    user_id: int
    questions: List[QuestionCreate]

class Exam(ExamBase):
    id: int
    questions: List[Question]
    class Config:
        orm_mode = True

class ExamSummary(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
