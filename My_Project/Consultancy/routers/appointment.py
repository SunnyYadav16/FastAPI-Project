from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from My_Project.Consultancy import database, models
from My_Project.Consultancy.JWT_token import get_current_active_user

from My_Project.Consultancy.schemas import ShowUser, ShowDoctor

appointment_router = APIRouter(
    tags=["Appointment"]
)
get_db = database.get_db
templates = Jinja2Templates(directory="My_Project/Consultancy/templates")


# @appointment_router.get("/appointment", response_class=HTMLResponse)
# def get_appointment(request: Request, db: Session = Depends(get_db)):
#     available_doctors = db.query(models.Doctor).filter(models.Doctor.is_active == True).all()
#     return templates.TemplateResponse("appointment.html", context={"request": request, "doctors": available_doctors})


@appointment_router.post("/create_appointment/")
async def create_appointment(db: Session = Depends(get_db),
                             appointment_date: datetime = datetime.now() + timedelta(hours=24),
                             description: str = Form(), selected_doctor: str = Form(),
                             current_user: ShowUser = Depends(get_current_active_user)):

    available_doctors = db.query(models.User).filter(models.User.is_active,
                                                     models.User.first_name == selected_doctor).first()

    appointment = models.Appointment(appointment_date=appointment_date, user_id=current_user.id,
                                     doctor_id=available_doctors.id, created_at=datetime.now(),
                                     description=description)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    # return templates.TemplateResponse("appointment.html", context={"request": request, "appointment": appointment})
    return {
        "message": f"Your appointment has been booked with doctor - {available_doctors.first_name} on {datetime.now() + timedelta(hours=24)}"}


@appointment_router.get("/get_patient_appointment/")
def get_patient_appointment(db: Session = Depends(get_db), current_user: ShowUser = Depends(get_current_active_user)):
    appointments = db.query(models.Appointment).filter(models.Appointment.doctor_id == current_user.id).all()
    # print(appointments[0].user.first_name)
    return {"appointments": appointments}


@appointment_router.put("/appointment/status/{id}")
def appointment_status(id: int, db: Session = Depends(get_db), is_approved_status: bool = Form(),
                       is_consulted_status: bool = Form()):
    appointments = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    appointments.is_approved = is_approved_status
    appointments.is_consulted = is_consulted_status
    appointments.updated_at = datetime.now()
    db.commit()
    db.refresh(appointments)
    return {"appointments": appointments}
