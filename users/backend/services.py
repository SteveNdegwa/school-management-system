from users.models import User, Role, RolePermission, Permission, TeacherProfile, StudentProfile, Guardian
from utils.ServiceBase import ServiceBase


class RoleService(ServiceBase):
    manager = Role.objects

class PermissionService(ServiceBase):
    manager = Permission.objects

class RolePermissionService(ServiceBase):
    manager = RolePermission.objects

class UserService(ServiceBase):
    manager = User.objects

class GuardianService(ServiceBase):
    manager = Guardian.objects

class StudentProfileService(ServiceBase):
    manager = StudentProfile.objects

class TeacherProfileService(ServiceBase):
    manager = TeacherProfile.objects
