from fastapi import FastAPI, HTTPException, Depends
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from sqlalchemy.orm import Session
from . import models, schemas, database

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
apm = make_apm_client({
    'SERVICE_NAME': 'user-service',
    'SECRET_TOKEN': os.getenv("APM_SECRET_TOKEN"),
    'SERVER_URL': os.getenv("APM_SERVER_URL"),
    'ENVIRONMENT': os.getenv("APM_ENVIRONMENT"),
})
app.add_middleware(ElasticAPM, client=apm)

models.Base.metadata.create_all(bind=database.engine)


@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
