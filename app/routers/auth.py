from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas, crud, authHelper, models, database
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=schemas.User)
def sign_up(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(database.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not authHelper.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=authHelper.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authHelper.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(authHelper.get_current_user)):
    return current_user

@router.post("/login", response_model=schemas.LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=form_data.username)
    if not db_user or not authHelper.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = authHelper.create_access_token(data={"sub": db_user.email})
    return {"user": db_user, "token": token}

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_users(db, user_id=user_id, user=user)

@router.put("/users/password/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_users_password(db, user_id=user_id, user=user)

@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id=user_id)

@router.get("/users/name/{name}", response_model=list[schemas.User])
def read_users_by_name(name: str, db: Session = Depends(database.get_db)):
    users = crud.get_users_by_name(db, name=name)
    return users


@router.post("/exams", response_model=schemas.Exam)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(database.get_db)):
    db_exam = crud.create_exam(db, exam=exam)
    for question in exam.questions:
        crud.create_question(db, question=question, exam_id=db_exam.id)
    return db_exam


@router.get("/users/{user_id}/exams", response_model=List[schemas.ExamSummary])
def read_user_exams(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_exams_by_user(db, user_id)


@router.get("/exams/{exam_id}", response_model=schemas.Exam)
def read_exam(exam_id: int, db: Session = Depends(database.get_db)):
    exam = crud.get_exam(db, exam_id)
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.delete("/exams/{exam_id}", response_model=schemas.Exam)
def delete_exam(exam_id: int, db: Session = Depends(database.get_db)):
    exam = crud.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # if exam.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to delete this exam")

    return crud.delete_exam(db, exam_id)
