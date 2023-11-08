import imp
from fastapi import FastAPI
import routers.auth as RouterAuth
from database import engine
from models import Base
import schemas
from fastapi import Depends
import auth

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(RouterAuth.router)

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user