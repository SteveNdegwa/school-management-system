import logging

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from base.models import GenericBaseModel, State, BaseModel
from users.managers import StudentManager, TeacherManager

lgr = logging.getLogger(__name__)
lgr.propagate = False

class Role(GenericBaseModel):
    state = models.ForeignKey(State, default=State.active, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

    @classmethod
    def admin(cls):
        try:
            return cls.objects.get(name="Admin")
        except Exception as e:
            lgr.exception("Role model - admin exception: %s" % e)
        return None

    @classmethod
    def student(cls):
        try:
            return cls.objects.get(name="Student")
        except Exception as e:
            lgr.exception("Role model - admin exception: %s" % e)
        return None

    @classmethod
    def teacher(cls):
        try:
            return cls.objects.get(name="Teacher")
        except Exception as e:
            lgr.exception("Role model - admin exception: %s" % e)
        return None

class Permission(GenericBaseModel):
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

class RolePermission(BaseModel):
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, null=True, blank=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.role.name, self.permission.name)

    class Meta:
        ordering = ('-date_created',)
        unique_together = ('role', 'permission')

class User(BaseModel, AbstractUser):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    DEFAULT_GENDER = "Other"
    DEFAULT_ROLE = Role.admin

    other_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, default=DEFAULT_GENDER, choices=GENDER)
    role = models.ForeignKey(Role, default=DEFAULT_ROLE, null=True, blank=True, editable=False, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=State.active, null=True, blank=True, on_delete=models.CASCADE)

    objects = UserManager()

    def __str__(self):
        return "%s %s - %s" % (self.first_name, self.last_name, self.role.name)

    class Meta:
        ordering = ('-date_created',)

class Student(User):
    DEFAULT_ROLE = Role.student
    objects = StudentManager

    class Meta:
        proxy = True


class Teacher(User):
    DEFAULT_ROLE = Role.teacher
    objects = TeacherManager

    class Meta:
        proxy = True

class Profile(BaseModel):
    pass
