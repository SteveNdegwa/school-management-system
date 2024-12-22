from users.models import User, Role, RolePermission, Permission, ExtendedPermission
from utils.ServiceBase import ServiceBase


class RoleService(ServiceBase):
    manager = Role.objects

class PermissionService(ServiceBase):
    manager = Permission.objects

class RolePermissionService(ServiceBase):
    manager = RolePermission.objects

class UserService(ServiceBase):
    manager = User.objects

class ExtendedPermissionService(ServiceBase):
    manager = ExtendedPermission.objects

