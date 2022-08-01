from typing import List, Optional

from pydantic import BaseModel


# USER SCHEMAS
class BaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class ShowUser(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


# DOCTOR'S SCHEMAS
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
