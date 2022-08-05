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
allow_create_resource = RoleChecker(["User"])


@user_routes.post("/retrieve_single_user/{email}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser,
                  dependencies=[Depends(allow_create_resource)])
async def retrieve_single_user(db: Session = Depends(get_db),
                               current_user: ShowUser = Depends(get_current_active_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    return user


@user_routes.get("/retrieve_user_appointment/{id}")
def retrieve_user_appointment(db: Session = Depends(get_db), current_user: ShowUser = Depends(get_current_active_user)):
    my_appointments = db.query(models.Appointment).filter(models.Appointment.user_id == current_user.id).all()
    return {"message": "Appointments retrieved successfully", "appointments": my_appointments}


@user_routes.put("/consultancy_rating/{id}")
def submit_consultancy_rating(id: int, rating: ModelName = Form(), db: Session = Depends(get_db),
                              current_user: ShowUser = Depends(get_current_active_user)):

    try:
        user_restrict = db.query(models.Appointment).filter(models.Appointment.user_id == current_user.id,
                                                            models.Appointment.doctor_id == id).first()
        if user_restrict.is_consulted:
            consult_rating = user_restrict.consultancy_rating

            if consult_rating is None and rating == "Like":
                consult_rating = "Like"
            elif consult_rating is None and rating == "Dislike":
                consult_rating = "Dislike"
            elif consult_rating == "Like" and rating == "Dislike":
                consult_rating = "Dislike"
            elif consult_rating == "Dislike" and rating == "Like":
                consult_rating = "Like"
            else:
                return {"message": "Rating already submitted!"}

            user_restrict.consultancy_rating = consult_rating
            db.commit()
            db.refresh(user_restrict)
            return {"message": "Rating submitted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not consulted with this doctor")

