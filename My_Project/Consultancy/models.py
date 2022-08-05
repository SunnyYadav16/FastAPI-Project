from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class ModelName(str, Enum):
    Like = "Like"
    Dislike = "Dislike"


class BaseClass(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    created_at = Column(DateTime())
    is_active = Column(Boolean, default=True)


class User(BaseClass):
    __tablename__ = "users"
    role_id = Column(Integer, ForeignKey("roles.id"))

    appointment_user = relationship("Appointment", back_populates="user", foreign_keys="Appointment.user_id")
    appointment_doctor = relationship("Appointment", back_populates="doctor", foreign_keys="Appointment.doctor_id")
    role = relationship("Role", back_populates="users")
    portfolio = relationship("DoctorPortfolio", back_populates="doctor")


class DoctorPortfolio(Base):
    __tablename__ = "doctor_portfolio"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    experience = Column(Integer)
    speciality = Column(String(100))
    description = Column(String(200))
    rating = Column(Integer, default=0)
    recommendation = Column(String(20), default="")

    doctor = relationship("User", back_populates="portfolio")


class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True, index=True)
    appointment_date = Column(DateTime())
    doctor_id = Column(Integer, ForeignKey("users.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    description = Column(String(200))
    is_approved = Column(Boolean, default=False)
    is_consulted = Column(Boolean, default=False)
    consultancy_rating = Column(String(10))

    doctor = relationship("User", foreign_keys=[doctor_id])
    user = relationship("User", foreign_keys=[user_id])


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100))

    users = relationship("User", back_populates="role")
