from typing import List, Optional

from pydantic import BaseModel


# USER SCHEMAS
class ShowAppointment(BaseModel):
    id: int
    appointment_date: str
    description: str
    is_approved: bool
    is_consulted: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    appointment: List[ShowAppointment] = []

    class Config:
        orm_mode = True


# DOCTOR'S SCHEMAS
class CreatePortfolio(BaseModel):
    experience: int
    speciality: str
    description: str
    rating: int
    recommendation: str

    class Config:
        orm_mode = True


class ShowDoctor(BaseModel):
    first_name: str
    last_name: str
    email: str
    portfolio: List[CreatePortfolio] = []

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: Optional[str] = None
