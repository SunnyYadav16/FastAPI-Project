from typing import List

from pydantic import BaseModel


# USER SCHEMAS
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


# DOCTOR'S SCHEMAS
class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class DoctorCreate(DoctorBase):
    password: str


class CreatePortfolio(BaseModel):
    experience: int
    speciality: str
    description: str

    class Config:
        orm_mode = True


class ShowDoctor(BaseModel):
    first_name: str
    last_name: str
    email: str
    portfolio: List[CreatePortfolio] = []

    class Config:
        orm_mode = True
