from base.models import State
from utils.ServiceBase import ServiceBase


class StateService(ServiceBase):
    manager = State.objects