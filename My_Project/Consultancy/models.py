from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


# class ModelName(str, Enum):
#     user = "User"
#     doctor = "Doctor"
#     admin = "Admin"


class BaseClass(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))


class User(BaseClass):
    __tablename__ = "users"
    created_at = Column(DateTime())
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    appointments = relationship("Appointment", back_populates="user")
    role = relationship("Role", back_populates="users")


class Doctor(BaseClass):
    __tablename__ = "doctors"
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    portfolio = relationship("DoctorPortfolio", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    role = relationship("Role", back_populates="doctors")


class DoctorPortfolio(Base):
    __tablename__ = "doctor_portfolio"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    experience = Column(Integer)
    speciality = Column(String(100))
    description = Column(String(200))
    doctor = relationship("Doctor", back_populates="portfolio")


class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True, index=True)
    appointment_date = Column(DateTime())
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    description = Column(String(200))
    is_approved = Column(Boolean, default=False)

    doctor = relationship("Doctor", back_populates="appointments")
    user = relationship("User", back_populates="appointments")


class Admin(BaseClass):
    __tablename__ = "admins"
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="admins")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100))

    users = relationship("User", back_populates="role")
    doctors = relationship("Doctor", back_populates="role")
    admins = relationship("Admin", back_populates="role")
