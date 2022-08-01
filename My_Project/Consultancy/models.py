from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class ModelName(str, Enum):
    user = "User"
    doctor = "Doctor"
    admin = "Admin"


class BaseClass(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    role = Column(String(100))


class User(BaseClass):
    __tablename__ = "users"
    created_at = Column(DateTime())
    is_active = Column(Boolean, default=True)


class Doctor(BaseClass):
    __tablename__ = "doctors"
    portfolio = relationship("DoctorPortfolio", back_populates="doctor")


class DoctorPortfolio(Base):
    __tablename__ = "doctor_portfolio"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    experience = Column(Integer)
    speciality = Column(String(100))
    description = Column(String(200))
    doctor = relationship("Doctor", back_populates="portfolio")


# class Appointment():
#     __tablename__ = "appointment"

class Admin(BaseClass):
    __tablename__ = "admins"
    is_active = Column(Boolean, default=True)
