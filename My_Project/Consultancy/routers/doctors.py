from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, database
from ..hashing import Hash

doctor_routes = APIRouter(
    tags=["Doctors"]
)
get_db = database.get_db


@doctor_routes.post("/register_doctor", status_code=status.HTTP_201_CREATED)
def create_doctor(request: schemas.DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = models.Doctor(first_name=request.first_name, last_name=request.last_name, email=request.email,
                               password=Hash.get_password_hash(request.password))
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@doctor_routes.post("/create_portfolio", status_code=status.HTTP_201_CREATED)
def create_portfolio(request: schemas.CreatePortfolio, db: Session = Depends(get_db)):
    new_portfolio = models.DoctorPortfolio(doctor_id=9, experience=request.experience,
                                           speciality=request.speciality, description=request.description)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio
