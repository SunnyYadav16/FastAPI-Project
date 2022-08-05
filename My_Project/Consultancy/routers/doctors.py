from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import schemas, models, database
from ..JWT_token import get_current_active_user
from ..Role_Check import RoleChecker
from ..models import User

doctor_routes = APIRouter(
    tags=["Doctors"]
)
get_db = database.get_db
allow_create_resource = RoleChecker(["Doctor"])


@doctor_routes.post("/create_portfolio", status_code=status.HTTP_201_CREATED,
                    dependencies=[Depends(allow_create_resource)])
async def create_portfolio(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user),
                           experience: int = Form(), speciality: str = Form(), description: str = Form()):

    new_portfolio = models.DoctorPortfolio(doctor_id=current_user.id, experience=experience,
                                           speciality=speciality, description=description)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return {"message": "Portfolio created successfully", "new_portfolio": new_portfolio}


# @doctor_routes.get("/retrieve_all_doctors", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowDoctor],
#                    dependencies=[Depends(allow_create_resource)])
# async def retrieve_all_doctors(db: Session = Depends(get_db)):
#     all_doctors = db.query(models.User).filter(models.User.role == 3).all()
#     return all_doctors


@doctor_routes.get("/retrieve_doctor_rating/", response_model=schemas.ShowDoctor, dependencies=[Depends(allow_create_resource)])
def retrieve_doctor_rating(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    doctor = db.query(models.DoctorPortfolio).filter(models.DoctorPortfolio.doctor_id == current_user.id).first()

    total_likes_count = db.query(func.count(models.Appointment.consultancy_rating)).filter(
        models.Appointment.doctor_id == current_user.id, models.Appointment.consultancy_rating == "Like").first()

    total_dislikes_count = db.query(func.count(models.Appointment.consultancy_rating)).filter(
        models.Appointment.doctor_id == current_user.id, models.Appointment.consultancy_rating == "Dislike").first()

    if total_dislikes_count[0] > total_likes_count[0]:
        doctor_rating = total_likes_count[0] - total_dislikes_count[0] * 10
    else:
        doctor_rating = abs(total_likes_count[0] - total_dislikes_count[0]) * 10

    if doctor_rating > 1000:
        doctor_recommendation = "Great Doctor"
    elif doctor_rating > 700:
        doctor_recommendation = "Good Doctor"
    elif doctor_rating > 500:
        doctor_recommendation = "Average Doctor"
    elif doctor_rating > 300:
        doctor_recommendation = "Bad Doctor"
    else:
        doctor_recommendation = "Very Bad Doctor"

    doctor.recommendation = doctor_recommendation
    doctor.rating = doctor_rating
    db.commit()
    db.refresh(doctor)

    my_ratings = db.query(models.User).filter(models.User.id == current_user.id).first()
    return my_ratings
