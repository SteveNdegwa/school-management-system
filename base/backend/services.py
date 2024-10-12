from base.models import State, TransactionType, Transaction, NotificationType, Notification
from utils.ServiceBase import ServiceBase


class StateService(ServiceBase):
    manager = State.objects

class TransactionTypeService(ServiceBase):
    manager = TransactionType.objects

class TransactionService(ServiceBase):
    manager = Transaction.objects

class NotificationTypeService(ServiceBase):
    manager = NotificationType.objects

class NotificationService(ServiceBase):
    manager = Notification.objects