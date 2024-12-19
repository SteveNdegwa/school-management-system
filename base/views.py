import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.backend.services import ClassRoomService, SchoolService
from base.models import State
from users.backend.decorators import user_login_required
from utils.get_request_data import get_request_data

lgr = logging.getLogger(__name__)

class BaseAdministration(object):
    @csrf_exempt
    @user_login_required
    def create_class(self, request):
        """
        Creates a class
        @param: WSGI Request
        @return: Success message and class_id or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            name = str(data.get("name", "")).title().strip()
            if not name:
                raise Exception("Name not provided")
            school_code = str(data.get("school", "")).lower()
            if not school_code:
                raise Exception("School code not provided")
            school = SchoolService().get(code=school_code, state=State.active())
            if not school:
                raise Exception("School not found")
            if ClassRoomService().filter(name=name, school=school, state=State.active()):
                raise Exception("Class room already exists")
            class_room = ClassRoomService().create(name=name, school=school)
            if not class_room:
                raise Exception("Class room not created")
            return JsonResponse({
                "code": "100.000.000", "message": "Class room created successfully",
                "class_room_id": str(class_room.id)})
        except Exception as e:
            lgr.exception("Create class room exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Create class room exception", "error": e})

    @csrf_exempt
    @user_login_required
    def edit_class(self, request):
        """
        Edits a class
        @param: WSGI Request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            class_room_id = data.get("class_room_id" , "")
            if not class_room_id:
                raise Exception("Class room id not provided")
            class_room = ClassRoomService().get(id=class_room_id, state=State.active())
            if not class_room:
                raise Exception("Class room not found")
            name = str(data.get("name", "")).title().strip()
            if not name:
                raise Exception("Name not provided")
            if ClassRoomService().filter(name=name, school=class_room.school, state=State.active()):
                raise Exception("Class room already exists")
            class_room = ClassRoomService().update(pk=class_room.id, name=name)
            if not class_room:
                raise Exception("Class room not edited")
            return JsonResponse({"code": "100.000.000", "message": "Class room edited successfully"})
        except Exception as e:
            lgr.exception("Edit class room exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Edit class room exception", "error": e})

