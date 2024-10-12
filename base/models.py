import logging
import uuid

from django.db import models

lgr = logging.getLogger(__name__)
lgr.propagate = False

class BaseModel(models.Model):
    id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = models.Manager

    class Meta:
        abstract = True

class GenericBaseModel(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

class State(GenericBaseModel):
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

    @classmethod
    def active(cls):
        try:
            return cls.objects.get(name="Active")
        except Exception as e:
            lgr.exception("State model - active exception: %s" % e)
        return None

