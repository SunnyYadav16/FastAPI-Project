from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from My_Project.Consultancy import database, schemas, models, oauth2
from My_Project.Consultancy.JWT_token import get_current_active_user
from My_Project.Consultancy.models import User
from My_Project.Consultancy.schemas import ShowUser

appointment_router = APIRouter(
    tags=["Appointment"]
)
get_db = database.get_db
templates = Jinja2Templates(directory="My_Project/Consultancy/templates")


# @appointment_router.get("/appointment", response_class=HTMLResponse)
# def get_appointment(request: Request, db: Session = Depends(get_db)):
#     available_doctors = db.query(models.Doctor).filter(models.Doctor.is_active == True).all()
#     return templates.TemplateResponse("appointment.html", context={"request": request, "doctors": available_doctors})


@appointment_router.post("/appointment")
async def get_appointment(db: Session = Depends(get_db), appointment_date: datetime = Form(),
                    description: str = Form(), selected_doctor: str = Form(),
                    current_user: ShowUser = Depends(get_current_active_user)):

    available_doctors = db.query(models.Doctor).filter(models.Doctor.is_active == True,
                                                       models.Doctor.first_name == selected_doctor).first()

    appointment = models.Appointment(appointment_date=datetime.now() + timedelta(hours=24), user_id=current_user.id,
                                     doctor_id=available_doctors.id, created_at=datetime.now(),
                                     description=description)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    # return templates.TemplateResponse("appointment.html", context={"request": request, "appointment": appointment})
    return {"message": f"Your appointment has been booked with doctor - {available_doctors.first_name} on {datetime.now() + timedelta(hours=24)}"}
