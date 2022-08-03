from My_Project.Consultancy import models
from My_Project.Consultancy.hashing import Hash


def get_user(db, email: str):
    user_dict = db.query(models.User).filter(models.User.email == email).first()
    return user_dict


def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not Hash.verify_password(password, user.password):
        return False
    return user
