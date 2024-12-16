import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.models import State
from users.backend.services import UserService, RoleService
from utils.common import generate_password, create_notification_detail
from utils.get_request_data import get_request_data
from utils.transaction_log_base import TransactionLogBase

lgr = logging.getLogger(__name__)
lgr.propagate = False

class UsersAdministration(TransactionLogBase):
    @csrf_exempt
    def create_user(self, request):
        """
        Creates a user
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        transaction = None
        try:
            transaction = self.log_transaction(transaction_type="CreateUser", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            email = data.get("email", "")
            phone_number = data.get("phone_number", "")
            if not email:
                raise Exception("Email address not provided")
            if not email or not phone_number:
                raise Exception("Phone number not provided")
            # TODO: GENERATE USERNAME AUTOMATICALLY
            username = ""
            role = RoleService().get(name=data.get("role", ""))
            if not role:
                raise Exception("Invalid role")
            data["role"] = role
            user = UserService().create(**data)
            if not user:
                raise Exception("User not created")
            password = generate_password()
            user.set_password(password)
            user.save()
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
    def deactivate_user(self, request):
        """
        Deactivates a user
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        transaction = None
        try:
            transaction = self.log_transaction("DeleteUser", request=request)
            if not transaction:
                raise Exception("Transaction log not created")
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                raise Exception("User does not exist")
            if not UserService().update(pk=user_id, state=State.inactive()):
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
            if not UserService().update(pk=user_id, **data):
                raise Exception("User not edited")
            return JsonResponse({"code": "100.000.000", "message": "User edited successfully"})
        except Exception as e:
            lgr.exception("Edit user exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Edit user failed with an exception", "error": e})
