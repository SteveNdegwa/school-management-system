import logging

from functools import wraps

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils import timezone

from base.models import State
from identities.backend.services import IdentityService
from users.backend.services import UserService, RoleService
from users.models import Role
from utils.get_request_data import get_request_data

lgr = logging.getLogger(__name__)


def user_login_required(inner_function):
    @wraps(inner_function)
    def _wrapped_function(*args, **kwargs):
        try:
            for k in args:
                if isinstance(k, WSGIRequest):
                    data = get_request_data(k)
                    token = data.get("token", "")
                    if not token:
                        return JsonResponse({"code": "888.888.001", "message": "Access token not provided"})
                    oauth = IdentityService().filter(
                        token=token, expires_at__gt=timezone.now(), state=State.active()).first()
                    if not oauth:
                        return JsonResponse({"code": "888.888.002", "message": "Not authenticated"})
                    oauth.extend()
                    return inner_function(*args, **kwargs)
        except Exception as e:
            lgr.exception("user_login_required decorator exception - %s" % str(e))
            return JsonResponse({"code": "888.888.888", "message": "Not authenticated"})
    return _wrapped_function

def super_admin(inner_function):
    @wraps(inner_function)
    def _wrapped_function(*args, **kwargs):
        try:
            for k in args:
                if isinstance(k, WSGIRequest):
                    data = get_request_data(k)
                    user_id = data.get("user_id", "")
                    user = UserService().get(id=user_id, state=State.active())
                    if user and user.role == Role.super_admin():
                        return inner_function(*args, **kwargs)
                    return JsonResponse({"code": "888.888.001", "message": "Not authorized"})
        except Exception as e:
            lgr.exception("superuser decorator exception - %s" % str(e))
            return JsonResponse({"code": "888.888.888", "message": "Not authorized"})
    return _wrapped_function

def admin(inner_function):
    @wraps(inner_function)
    def _wrapped_function(*args, **kwargs):
        try:
            for k in args:
                if isinstance(k, WSGIRequest):
                    data = get_request_data(k)
                    user_id = data.get("user_id", "")
                    user = UserService().get(id=user_id, state=State.active())
                    if user and user.role in [Role.super_admin(), Role.admin()]:
                        return inner_function(*args, **kwargs)
                    return JsonResponse({"code": "888.888.001", "message": "Not authorized"})
        except Exception as e:
            lgr.exception("superuser decorator exception - %s" % str(e))
            return JsonResponse({"code": "888.888.888", "message": "Not authorized"})
    return _wrapped_function
