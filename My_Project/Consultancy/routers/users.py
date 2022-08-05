from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from My_Project.Consultancy import database, schemas, models
from My_Project.Consultancy.JWT_token import get_current_active_user
from My_Project.Consultancy.Role_Check import RoleChecker
from My_Project.Consultancy.models import ModelName
from My_Project.Consultancy.schemas import ShowUser

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

allow_create_resource = RoleChecker(["User"])


@user_routes.post("/retrieve_single_user/{email}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser,
                  dependencies=[Depends(allow_create_resource)])
async def retrieve_single_user(db: Session = Depends(get_db),
                               current_user: schemas.ShowUser = Depends(get_current_active_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    return user


@user_routes.get("/retrieve_user_appointment/{id}")
def retrieve_user_appointment(db: Session = Depends(get_db), current_user: ShowUser = Depends(get_current_active_user)):
    my_appointments = db.query(models.Appointment).filter(models.Appointment.user_id == current_user.id).all()
    return {"message": "Appointments retrieved successfully", "appointments": my_appointments}


@user_routes.put("/doctor_rating/{id}", response_model=schemas.ShowDoctor)
def submit_doctor_rating(id: int, rating: ModelName = Form(), db: Session = Depends(get_db)):
    my_ratings = db.query(models.User).filter(models.User.id == id).first()
    current_rating = my_ratings.portfolio[0].rating

    if rating == "Like":
        current_rating += 1
    else:
        current_rating -= 1

    updated_rating = db.query(models.DoctorPortfolio).filter(models.DoctorPortfolio.doctor_id == id).first()
    updated_rating.rating = current_rating
    db.commit()
    db.refresh(updated_rating)
    return my_ratings
