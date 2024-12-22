import logging

from django.db import transaction as trx
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.backend.services import SchoolService, ClassroomService
from base.models import State
from users.backend.decorators import user_login_required, super_admin, admin
from users.backend.services import UserService
from users.models import Role
from utils.common import generate_password, create_notification_detail
from utils.get_request_data import get_request_data
from utils.transaction_log_base import TransactionLogBase

lgr = logging.getLogger(__name__)
lgr.propagate = False

class UsersAdministration(TransactionLogBase):
    @csrf_exempt
    @user_login_required
    @super_admin
    def create_super_admin(self, request:object):
        """
        Creates a super admin
        """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateSuperAdmin", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            data.pop("user_id", "")
            data.pop("token", "")
            data.update({"role": Role.super_admin(), "is_superuser": True, "is_staff": True})
            return self.create_user(data=data, transaction=transaction)
        except Exception as e:
            lgr.exception("Create super admin exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    @user_login_required
    @super_admin
    def create_admin(self, request: object):
        """
        Creates an admin
        """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateAdmin", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            data.pop("user_id", "")
            data.pop("token", "")
            data.update({"role": Role.admin(), "is_superuser": False, "is_staff": False})
            return self.create_user(data=data, transaction=transaction)
        except Exception as e:
            lgr.exception("Create admin exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    @user_login_required
    @admin
    def create_clerk(self, request: object):
        """
        Creates a clerk
        """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateClerk", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            data.pop("user_id", "")
            data.pop("token", "")
            data.update({"role": Role.clerk(), "is_superuser": False, "is_staff": False})
            return self.create_user(data=data, transaction=transaction)
        except Exception as e:
            lgr.exception("Create clerk exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    @user_login_required
    def create_student(self, request: object):
        """
        Creates a student
        """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateStudent", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            data.pop("user_id", "")
            data.pop("token", "")
            classroom_id = data.get("classroom_id", '')
            if not classroom_id:
                raise Exception("Classroom id not provided")
            classroom = ClassroomService().get(id=classroom_id, state=State.active())
            if not classroom:
                raise Exception("Classroom not found")
            data.update({"role": Role.student(), "classroom":classroom, "is_superuser": False, "is_staff": False})
            return self.create_user(data=data, transaction=transaction)
        except Exception as e:
            lgr.exception("Create student exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    @user_login_required
    def create_teacher(self, request: object):
        """
        Creates a teacher
        """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateTeacher", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            data.pop("user_id", "")
            data.pop("token", "")
            data.update({"role": Role.teacher(), "is_superuser": False, "is_staff": False})
            return self.create_user(data=data, transaction=transaction)
        except Exception as e:
            lgr.exception("Create teacher exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @trx.atomic
    def create_user(self, data:dict, transaction:object):
        """
        Creates a user
        @params: user data, transaction log
        @return: success or failure message
        @rtype: JsonResponse
        """
        try:
            email = data.get("email", "")
            phone_number = data.get("phone_number", "")
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            school_code = data.get("school", "")

            # Verify all required details are provided
            if not email:
                raise Exception("Email address not provided")
            if not phone_number:
                raise Exception("Phone number not provided")
            if not first_name:
                raise Exception("First name not provided")
            if not last_name:
                raise Exception("Last name not provided")
            if not school_code:
                raise Exception("School code not provided")

            # check if school is valid
            school = SchoolService().get(code=school_code, state=State.active())
            if not school:
                raise Exception("School not found")
            data["school"] = school

            # Generate username
            # TODO: GENERATE USERNAME AUTOMATICALLY
            username = ""

            # Create user
            user = UserService().create(**data)
            if not user:
                raise Exception("User not created")
            password = generate_password()
            user.set_password(password)
            user.save()

            # Create notification
            notification_msg = "Welcome, use your username - %s  and password - %s to login" % (username, password)
            notification_details = create_notification_detail(
                message_code="SC0009", message_type="2", message=notification_msg, destination=user.email)

            response = {"code": "100.000.000", "message": "User created successfully"}
            self.complete_transaction(transaction, response=response, notification_details=notification_details)
            return JsonResponse(response)
        except Exception as e:
            lgr.exception("Create user exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    @user_login_required
    def deactivate_user(self, request):
        """
        Deactivates a user
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        transaction = None
        try:
            transaction = self.log_transaction("DeactivateUser", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                raise Exception("User does not exist")
            if not UserService().update(pk=user.id, classroom=None, state=State.inactive()):
               raise Exception("User not deactivated")
            notification_msg = "User, username: %s has been deactivated successfully" % user.username
            notification_details = create_notification_detail(
                message_code="SC0009", message_type="2", message=notification_msg, destination=user.email)
            response = {"code": "100.000.000", "message": "User deactivated successfully"}
            self.complete_transaction(transaction, response=response, notification_details=notification_details)
            return JsonResponse(response)
        except Exception as e:
            lgr.exception("Deactivate user exception: %s" % e)
            response = {"code": "999.999.999", "message": "Deactivate user failed with an exception", "error": e}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    @user_login_required
    def edit_user(self, request):
        """
        Edits a user's details
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            user_id = data.pop("user_id", "")
            data.pop("token", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                raise Exception("User not found")
            if "classroom_id" in data:
                classroom_id = data.pop("classroom_id")
                classroom = ClassroomService().get(id=classroom_id, state=State.active())
                if not classroom:
                    raise Exception("Classroom not found")
                data["classroom"] = classroom
            if not UserService().update(pk=user.id, **data):
                raise Exception("User not edited")
            return JsonResponse({"code": "100.000.000", "message": "User edited successfully"})
        except Exception as e:
            lgr.exception("Edit user exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Edit user failed with an exception", "error": e})
