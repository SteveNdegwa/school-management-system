import logging

from django.db import transaction as trx
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.backend.services import SchoolService, ClassroomService, StateService
from base.models import State
from users.backend.decorators import user_login_required, super_admin, admin
from users.backend.services import UserService, RoleService
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
            school_id = data.pop("school_id", "")
            if not email:
                raise Exception("Email address not provided")
            if not phone_number:
                raise Exception("Phone number not provided")
            if not first_name:
                raise Exception("First name not provided")
            if not last_name:
                raise Exception("Last name not provided")
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            data["school"] = school
            # TODO: GENERATE USERNAME AUTOMATICALLY
            username = ""
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
            user = UserService().get(id=user_id)
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
    def get_user(self, request):
        """
        Fetches a user's details
        @params: WSGI Request
        @return: success message and user data or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            if not user_id:
                raise Exception("User id not provided")
            user = UserService().get(id=user_id)
            if not user:
                raise Exception("User not found")
            user_data = UserService().filter(id=user_id).annotate(role_name=F("role__name")) \
                .annotate(state__name=F("state__name")).values(
                "id", "username", "email", "phone_number", "other_phone_number", "first_name", "last_name",
                "other_name", "gender", "id_no", "reg_no", "school_id", "classroom_id", "role_name", "state_name")
            user_data["permissions"] = user.permissions
            return JsonResponse({"code": "100.000.000", "message": "Successfully fetched user", "data": user_data})
        except Exception as e:
            lgr.exception("Get user exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get user failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def filter_users(self, request):
        """
        Filters users
        @params: WSGI Request
        @return: success message and user data or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            data.pop("token", "")
            data.pop("user_id", "")
            school_id = data.pop("school_id", "")
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            data["school"] = school
            if not school:
                raise Exception("School not found")
            if "classroom_id" in data:
                classroom_id = data.pop("classroom_id", "")
                classroom = ClassroomService().get(id=classroom_id, state=State.active())
                data["classroom"] = classroom
            if "role_name" in data:
                role_name = data.pop("role_name", "")
                role = RoleService().get(name=role_name, state=State.active())
                data["role"] = role
            if "state_name" in data:
                state_name = data.pop("state_name", "")
                state = StateService().get(id=state_name)
                data["state"] = state
            users_data = UserService().filter(**data).annotate(role_name=F("role__name")) \
                .annotate(state__name=F("state__name")).values(
                "id", "username", "email", "phone_number", "other_phone_number", "first_name", "last_name",
                "other_name", "gender", "id_no", "reg_no", "school_id", "classroom_id", "role_name", "state_name")
            users_data = list(users_data)
            return JsonResponse({"code": "100.000.000", "message": "Successfully filtered users", "data": users_data})
        except Exception as e:
            lgr.exception("Filter users exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Filter users failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def search_users(self, request):
        """
        Search users
        @params: WSGI Request
        @return: success message and user data or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            school_id = data.get("school_id", "")
            search_word = data.get("search_word", "")
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            users_data = UserService().filter(
                school=school, first_name__icontains=search_word, last_name__icontains=search_word,
                other_name__icontains=search_word, email__icontains=search_word, phone_number__icontains=search_word,
                other_phone_number__icontains=search_word, id_no__icontains=search_word, reg_no__icontains=search_word,
                gender__icontains=search_word).annotate(role_name=F("role__name")) \
                .annotate(state__name=F("state__name")).values(
                "id", "username", "email", "phone_number", "other_phone_number", "first_name", "last_name",
                "other_name", "gender", "id_no", "reg_no", "school_id", "classroom_id", "role_name", "state_name")
            users_data = list(users_data)
            return JsonResponse({"code": "100.000.000", "message": "Successfully searched users", "data": users_data})
        except Exception as e:
            lgr.exception("Search users exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Search users failed with an exception", "error": e})
