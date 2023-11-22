from sqlalchemy.orm import Session
# from . import models, schemas, auth
import models, schemas, authHelper as auth

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_users(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def update_users_password(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.hashed_password = auth.get_password_hash(user.password)
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

def get_users_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).all()



def create_exam(db: Session, exam: schemas.ExamCreate):
    db_exam = models.Exam(name=exam.name, user_id=exam.user_id)
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam

def create_question(db: Session, question: schemas.QuestionCreate, exam_id: int):
    db_question = models.Question(**question.dict(), exam_id=exam_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_exams_by_user(db: Session, user_id: int):
    return db.query(models.Exam).filter(models.Exam.user_id == user_id).all()


def get_exam(db: Session, exam_id: int):
    return db.query(models.Exam).filter(models.Exam.id == exam_id).first()

def delete_exam(db: Session, exam_id: int):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if exam:
        db.delete(exam)
        db.commit()
        return exam
    else:
        return None 
