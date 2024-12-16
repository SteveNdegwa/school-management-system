from utils.ServiceBase import ServiceBase
from identities.models import Identity

class IdentityService(ServiceBase):
    manager = Identity.objects

