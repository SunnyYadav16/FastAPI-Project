from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models, database

admin_routes = APIRouter(
    tags=["Admin"]
)
get_db = database.get_db


@admin_routes.get("/user-list", response_model=List[schemas.ShowUser])
async def get_user_list(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users


@admin_routes.get("/doctor-list", response_model=List[schemas.ShowDoctor])
async def get_doctor_list(db: Session = Depends(get_db)):
    all_doctors = db.query(models.Doctor).all()
    return all_doctors
