from fastapi import FastAPI

from My_Project.Consultancy.database import engine
from My_Project.Consultancy.routers import users, doctors, admin
from My_Project.Consultancy import models

app = FastAPI()

models.Base.metadata.create_all(engine)  # Create the tables

app.include_router(users.user_routes)
app.include_router(doctors.doctor_routes)
app.include_router(admin.admin_routes)
