from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from My_Project.Consultancy import database, models, schemas
from My_Project.Consultancy.JWT_token import create_access_token
from My_Project.Consultancy.hashing import Hash
from My_Project.Consultancy.models import ModelName

auth_router = APIRouter(
    tags=["Authentication"]
)
get_db = database.get_db


@auth_router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # access_token_expires = timedelta(minutes - ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        # expires_delta - access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register/{new_member}", response_model=schemas.ShowUser)
def register(new_member: ModelName, request: schemas.BaseSchema, db: Session = Depends(get_db)):

    if new_member == ModelName.user:
        new_user = models.User(first_name=request.first_name, last_name=request.last_name,
                               email=request.email, password=Hash.get_password_hash(request.password),
                               created_at=datetime.now(), is_active=True, role=ModelName.user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    elif new_member == ModelName.doctor:
        new_doctor = models.Doctor(first_name=request.first_name, last_name=request.last_name,
                                   email=request.email, password=Hash.get_password_hash(request.password),
                                   role=ModelName.doctor)
        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)
        return new_doctor

    else:
        new_admin = models.Admin(first_name=request.first_name, last_name=request.last_name,
                                 email=request.email, password=Hash.get_password_hash(request.password),
                                 role=ModelName.admin)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin

