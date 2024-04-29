import uuid

from django.db import models

from eusers.models import EUser


# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GenericBaseModel(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class State(GenericBaseModel):
    def __str__(self):
        return self.name

    @classmethod
    def default_state(cls):
        try:
            state = cls.objects.get(state="Active")
            return state
        except Exception:
            pass
        return None


class Role(GenericBaseModel):
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Permission(GenericBaseModel):
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RolePermission(BaseModel):
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, null=True, blank=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s", (self.role.name, self.permission.name)


class TransactionType(GenericBaseModel):
    def __str__(self):
        return self.name


class Transaction(BaseModel):
    euser = models.ForeignKey(EUser, null=True, blank=True, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    source_ip = models.CharField(max_length=100, null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    response_code = models.CharField(max_length=20, null=True, blank=True)
    notification_response = models.TextField(null=True, blank=True)
    record = models.CharField(max_length=400, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.euser, self.transaction_type)
