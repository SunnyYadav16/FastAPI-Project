from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models, database
from ..Role_Check import RoleChecker

admin_routes = APIRouter(
    tags=["Admin"]
)
get_db = database.get_db
allow_create_resource = RoleChecker(["Admin"])


@admin_routes.get("/user-list", response_model=List[schemas.ShowUser], dependencies=[Depends(allow_create_resource)])
async def get_user_list(db: Session = Depends(get_db)):
    all_users = db.query(models.User).filter(models.User.role_id == 2).all()
    return all_users


@admin_routes.get("/doctor-list", response_model=List[schemas.ShowDoctor], dependencies=[Depends(allow_create_resource)])
async def get_doctor_list(db: Session = Depends(get_db)):
    all_doctors = db.query(models.User).filter(models.User.role_id == 3).all()
    return all_doctors
