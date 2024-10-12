from users.models import User, Student, Teacher, Role, RolePermission, Permission
from utils.ServiceBase import ServiceBase


class RoleService(ServiceBase):
    manager = Role.objects

class PermissionService(ServiceBase):
    manager = Permission.objects

class RolePermissionService(ServiceBase):
    manager = RolePermission.objects

class UserService(ServiceBase):
    manager = User.objects

class StudentService(ServiceBase):
    manager = Student.objects

class TeacherService(ServiceBase):
    manager = Teacher.objects