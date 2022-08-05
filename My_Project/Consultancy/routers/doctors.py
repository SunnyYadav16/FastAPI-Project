from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, models, database
from ..JWT_token import get_current_active_user
from ..Role_Check import RoleChecker

doctor_routes = APIRouter(
    tags=["Doctors"]
)
get_db = database.get_db
allow_create_resource = RoleChecker(["Doctor"])


# @doctor_routes.post("/register_doctor", status_code=status.HTTP_201_CREATED)
# def create_doctor(request: schemas.DoctorCreate, db: Session = Depends(get_db)):
#     new_doctor = models.Doctor(first_name=request.first_name, last_name=request.last_name, email=request.email,
#                                password=Hash.get_password_hash(request.password))
#     db.add(new_doctor)
#     db.commit()
#     db.refresh(new_doctor)
#     return new_doctor


@doctor_routes.post("/create_portfolio", status_code=status.HTTP_201_CREATED,
                    dependencies=[Depends(allow_create_resource)])
async def create_portfolio(request: schemas.CreatePortfolio, db: Session = Depends(get_db), current_user: schemas.ShowDoctor = Depends(get_current_active_user)):
    new_portfolio = models.DoctorPortfolio(doctor_id=current_user.id, experience=request.experience,
                                           speciality=request.speciality, description=request.description)
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
def retrieve_doctor_rating(db: Session = Depends(get_db), current_user: schemas.ShowDoctor = Depends(get_current_active_user)):
    my_ratings = db.query(models.User).filter(models.User.id == current_user.id).first()
    return my_ratings

