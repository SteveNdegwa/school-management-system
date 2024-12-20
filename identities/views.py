import calendar
import logging

from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from base.models import State
from identities.backend.services import IdentityService
from users.backend.services import UserService
from utils.common import create_notification_detail, get_client_ip
from utils.generate_system_aoth_otp import OAuthHelper
from utils.get_request_data import get_request_data
from utils.transaction_log_base import TransactionLogBase

lgr = logging.getLogger(__name__)
lgr.propagate = False


class IdentitiesAdministration(TransactionLogBase):
    @csrf_exempt
    def login(self, request):
        """
        Logs in a user using username and password
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            username = str(data.get("username", "")).lower()
            if not username:
                raise Exception("Username not provided")
            password = data.get("password", "")
            if not password:
                raise Exception("Password not provided")
            source_ip = get_client_ip(request)
            user = UserService().get(username=username)
            if not user:
                raise Exception("User not found")
            if not user.check_password(password):
                raise Exception("Wrong credentials")
            IdentityService().filter(
                user=user, state=State.active(), expires_at__lt=timezone.now()).update(state=State.expired())
            oauth = IdentityService().filter(user=user, state=State.active(), expires_at__gt=timezone.now()).first()
            if not oauth:
                oauth = IdentityService().create(user=user, source_ip=source_ip, state=State.activation_pending())
                if not oauth:
                    raise Exception("Identity not created")
                oauth_today = IdentityService().filter(
                    user=user, date_created__date=timezone.now().date(), state=State.expired()).first()
                if not oauth_today:
                    generated = OAuthHelper.generate_device_otp()
                    otp = list(generated)
                    key = (otp[1]).decode()
                    oauth = IdentityService().update(pk=oauth.id, totp_key=key, totp_time_value=otp[2])
                    totp = otp[0]
                    if not oauth:
                        raise Exception("Identity not updated")
                    notification_msg = "Welcome. Your OTP is %s" % totp.decode()
                    notification_details = create_notification_detail(
                        message_code="SC0009", message_type="2", message=notification_msg, destination=user.email)
                    self.send_notification(notifications=notification_details)
                else:
                    oauth = IdentityService().update(
                        pk=oauth.id, otp_key=oauth_today.totp_key, totp_time_value=oauth_today.totp_time_value)
                    if not oauth:
                        raise Exception("Identity not updated")
            oauth = oauth.extend()
            user.update_last_activity()
            return JsonResponse({
                "code": "100.000.000",
                "message": "Login successful",
                "data": {
                    "token": str(oauth.token),
                    "user_id": str(user.id),
                    "expires_at": calendar.timegm(oauth.expires_at.timetuple())
                }
            })
        except Exception as e:
            lgr.exception("Login exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Login failed with an exception"})

    @csrf_exempt
    def verify_totp(self, request):
        """
        Verifies the TOTP of a user
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            token = data.get("token", "")
            totp = data.get("otp", "")
            oauth = IdentityService().filter(
                ~Q(user=None), state__in=[State.active(), State.activation_pending()], token=token,
                expires_at__gt=timezone.now()).first()
            if not oauth:
                raise Exception("Identity not found")
            generated = OAuthHelper.verify_device(oauth.totp_key, str(totp).strip(), float(oauth.totp_time_value))
            if not generated:
                raise Exception("Invalid OTP")
            oauth = IdentityService().update(pk=oauth.id, state=State.active())
            if not oauth:
                raise Exception("Identity not updated")
            oauth = oauth.extend()
            return JsonResponse({
                "code": "100.000.000",
                "message": "OTP verified",
                "data": {
                    "activated": True,
                    "expires_at": calendar.timegm(oauth.expires_at.timetuple())
                }
            })
        except Exception as e:
            lgr.exception("Verify totp exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Verify totp failed with an exception", "error": e})

    @csrf_exempt
    def logout(self, request):
        """
        Logs out out a user
        @params: WSGI Request
        @return: success or failure message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                raise Exception("User not found")
            IdentityService().filter(user=user, state=State.active()).update(state=State.expired())
            return JsonResponse({"code": "100.000.000", "message": "User logged out successfully"})
        except Exception as e:
            lgr.exception("Logout exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Logout failed with an exception", "error": e})


