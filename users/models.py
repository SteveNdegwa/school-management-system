import logging

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from base.models import GenericBaseModel, State, BaseModel

lgr = logging.getLogger(__name__)
lgr.propagate = False

class Role(GenericBaseModel):
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

    @classmethod
    def admin(cls):
        try:
            role, created = cls.objects.get_or_create(name="Admin")
            return role
        except Exception as e:
            lgr.exception("Role model - admin exception: %s" % e)
            return None

    @classmethod
    def student(cls):
        try:
            role, created = cls.objects.get_or_create(name="Student")
            return role
        except Exception as e:
            lgr.exception("Role model - student exception: %s" % e)
            return None

    @classmethod
    def teacher(cls):
        try:
            role, created = cls.objects.get_or_create(name="Teacher")
            return role
        except Exception as e:
            lgr.exception("Role model - teacher exception: %s" % e)
            return None

class Permission(GenericBaseModel):
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

class RolePermission(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.role, self.permission)

    class Meta:
        ordering = ('-date_created',)
        unique_together = ('role', 'permission')


class User(BaseModel, AbstractUser):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    DEFAULT_GENDER = "other"
    DEFAULT_ROLE = Role.admin

    other_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, default=DEFAULT_GENDER, choices=GENDER)
    id_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
    reg_no = models.CharField(max_length=20, editable=False, unique=True)
    tsc_no = models.CharField(max_length=20, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    other_phone_number = models.CharField(max_length=100, blank=True, null=True)
    role = models.ForeignKey(Role, default=DEFAULT_ROLE, editable=False, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    objects = UserManager()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ('-date_created',)

class ExtendedPermission(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user, self.permission)

    class Meta:
        ordering = ('-date_created',)