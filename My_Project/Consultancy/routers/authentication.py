from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from My_Project.Consultancy import database, models, schemas, oauth2
from My_Project.Consultancy.JWT_token import create_access_token, ACCESS_TOKEN_EXPIRE_HOURS, get_current_active_user
from My_Project.Consultancy.hashing import Hash
from My_Project.Consultancy.schemas import Token, ShowUser

auth_router = APIRouter(
    tags=["Authentication"]
)
get_db = database.get_db
templates = Jinja2Templates(directory="My_Project/Consultancy/templates")


@auth_router.get("/Get_Current_User_Details/")
async def read_items(current_user: ShowUser = Depends(get_current_active_user)):
    return {"current_user": current_user.first_name, "current_user_email": current_user.email}


# @auth_router.get("/token", response_class=HTMLResponse)
# def login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/token", response_model=Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = oauth2.authenticate_user(db, request.username, request.password)
    if not user or not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # access_token_expires = timedelta(minutes - ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"message": f"Logged in successfully!", "access_token": access_token, "token_type": "bearer"}


# @auth_router.get("/register/form/", response_class=HTMLResponse)
# def register(request: Request, db: Session = Depends(get_db)):
#     role = db.query(models.Role).all()
#     return templates.TemplateResponse("register.html", {"request": request, 'roles': role})


# @auth_router.post("/register/form/", response_class=HTMLResponse)
@auth_router.post("/register/form/")
async def register(db: Session = Depends(get_db), first_name: str = Form(),
                   last_name: str = Form(), email: str = Form(), password: str = Form(), role: str = Form()):

    registered_role = db.query(models.Role).filter(models.Role.role_name == role).first()
    new_user = models.User(first_name=first_name, last_name=last_name,
                           email=email, password=Hash.get_password_hash(password),
                           created_at=datetime.now(), is_active=True, role_id=registered_role.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return templates.TemplateResponse("login.html", context={"request": request, "user": new_user})
    return {"message": f"User {new_user.first_name} {new_user.last_name} registered successfully"}
