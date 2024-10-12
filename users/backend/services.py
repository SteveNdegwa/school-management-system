from users.models import User, Role, RolePermission, Permission
from utils.ServiceBase import ServiceBase


class RoleService(ServiceBase):
    manager = Role.objects

class PermissionService(ServiceBase):
    manager = Permission.objects

class RolePermissionService(ServiceBase):
    manager = RolePermission.objects

class UserService(ServiceBase):
    manager = User.objects