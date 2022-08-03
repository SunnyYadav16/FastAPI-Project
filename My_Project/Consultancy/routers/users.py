from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from My_Project.Consultancy import database, schemas, models

user_routes = APIRouter(
    tags=["Users"]
)
get_db = database.get_db


# @user_routes.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
# def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
#     new_user = models.User(first_name=request.first_name, last_name=request.last_name, email=request.email,
#                            password=Hash.get_password_hash(request.password), created_at=datetime.now(), is_active=True)
#     # if not new_user:
#     #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Registration Error")
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


@user_routes.post("/retrieve_single_user/{email}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
async def retrieve_user(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    return {"message": "User retrieved successfully", "user": user}


@user_routes.get("/retrieve_all_users", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
async def retrieve_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users
