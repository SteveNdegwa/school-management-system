from base.models import State, TransactionType, Transaction, NotificationType, Notification, Classroom, School, Subject
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

class SchoolService(ServiceBase):
    manager = School.objects

class ClassroomService(ServiceBase):
    manager = Classroom.objects

class SubjectService(ServiceBase):
    manager = Subject.objects