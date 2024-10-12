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
                return JsonResponse({"code": "999.999.001", "message": "Transaction not created"})
            data = get_request_data(request)
            username = data.get("username", "")
            email = data.get("email", "")
            phone_number = data.get("phone_number", "")
            if not username or not email or not phone_number:
                response = {"code": "999.999.002", "message": "Provide all required details"}
                self.mark_transaction_failed(transaction=transaction, response=response)
            if UserService().get(username=username, state=State.active()):
                response = {"code": "999.999.003", "message": "Username already exists"}
                self.mark_transaction_failed(transaction, response=response)
                return JsonResponse(response)
            role = RoleService().get(name=data.get("role", ""))
            if not role:
                response = {"code": "999.999.004", "message": "Invalid role"}
                self.mark_transaction_failed(transaction, response=response)
                return JsonResponse(response)
            data.update({"role": role})
            user = UserService().create(**data)
            if not user:
                response = {"code": "999.999.005", "message": "User not created"}
                self.mark_transaction_failed(transaction, response=response)
                return JsonResponse(response)
            password = generate_password()
            user.set_password(password)
            notification_msg = "Welcome, use your username - %s  and password - %s to login" % (username, password)
            notification_details = create_notification_detail(
                message_code="SC0009", message_type="2", message=notification_msg, destination=user.email)
            response = {"code": "100.000.000", "message": "User created successfully"}
            self.complete_transaction(transaction, response=response, notification_details=notification_details)
            return JsonResponse(response)
        except Exception as e:
            lgr.exception("Create user exception: %s" % e)
            response = {"code": "999.999.999", "message": "Create user failed with an exception"}
            self.mark_transaction_failed(transaction, response=response)
            return JsonResponse(response)

    @csrf_exempt
    def deactivate_user(self, request):
        """
        Deletes a user
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        transaction = None
        try:
            transaction = self.log_transaction("DeleteUser", request=request)
            if not transaction:
                return JsonResponse({"code": "999.999.001", "message": "Transaction not created"})
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                response = {"code": "999.999.002", "message": "User not found"}
                self.mark_transaction_failed(transaction, response=response)
                return JsonResponse(response)
            if not UserService().update(pk=user_id, state=State.inactive()):
                response = {"code": "999.999.003", "message": "User not deactivated"}
                self.mark_transaction_failed(transaction, response=response)
                return JsonResponse(response)
            notification_msg = "Your account has been deactivated successfully"
            notification_details = create_notification_detail(
                message_code="SC0009", message_type="2", message=notification_msg, destination=user.email)
            response = {"code": "100.000.000", "message": "User deactivated successfully"}
            self.complete_transaction(transaction, response=response, notification_details=notification_details)
            return JsonResponse(response)
        except Exception as e:
            lgr.exception("Deactivate user exception: %s" % e)
            response = {"code": "999.999.999", "message": "Deactivate user failed with an exception"}
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
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                return JsonResponse({"code": "999.999.001", "message": "User not found"})
            if not UserService().update(pk=user_id, **data):
                return JsonResponse({"code": "999.999.003", "message": "User not edited"})
            return JsonResponse({"code": "100.000.000", "message": "User edited successfully"})
        except Exception as e:
            lgr.exception("Edit user exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Edit user failed with an exception"})
