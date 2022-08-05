from typing import List

from fastapi import Depends, HTTPException

from My_Project.Consultancy.JWT_token import get_current_active_user
from My_Project.Consultancy.models import User


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role.role_name not in self.allowed_roles:
            print(f"User with role {user.role.role_name} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail=f"Operation not permitted for this {user.role.role_name}")


# class DoctorRoleChecker:
#     def __init__(self, allowed_roles: List):
#         self.allowed_roles = allowed_roles
#
#     def __call__(self, doctor: Doctor = Depends(get_current_active_user)):
#         if doctor.role.role_name not in self.allowed_roles:
#             print(f"User with role {doctor.role.role_name} not in {self.allowed_roles}")
#             raise HTTPException(status_code=403, detail=f"Operation not permitted for this {doctor.role.role_name}")
#
#
# class AdminRoleChecker:
#     def __init__(self, allowed_roles: List):
#         self.allowed_roles = allowed_roles
#
#     def __call__(self, admin: Admin = Depends(get_current_active_user)):
#         if admin.role.role_name not in self.allowed_roles:
#             print(f"User with role {admin.role.role_name} not in {self.allowed_roles}")
#             raise HTTPException(status_code=403, detail=f"Operation not permitted for this {admin.role.role_name}")