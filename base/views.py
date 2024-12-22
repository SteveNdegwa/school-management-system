import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.backend.services import ClassroomService, SchoolService, SubjectService
from base.models import State
from users.backend.decorators import user_login_required
from users.backend.services import UserService
from utils.get_request_data import get_request_data

lgr = logging.getLogger(__name__)

class BaseAdministration(object):
    @csrf_exempt
    @user_login_required
    def create_classroom(self, request):
        """
        Creates a classroom
        @param: WSGI Request
        @return: Success message and classroom_id or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            name = str(data.get("name", "")).title().strip()
            if not name:
                raise Exception("Name not provided")
            school_id = str(data.get("school_id", "")).lower()
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(code=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            if ClassroomService().filter(name=name, school=school, state=State.active()):
                raise Exception("Classroom already exists")
            classroom = ClassroomService().create(name=name, school=school)
            if not classroom:
                raise Exception("Classroom not created")
            return JsonResponse({
                "code": "100.000.000", "message": "Classroom created successfully",
                "classroom_id": str(classroom.id)})
        except Exception as e:
            lgr.exception("Create classroom exception: %s" % e)
            return JsonResponse({
                "code": "999.999.999", "message": "Create classroom failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def edit_classroom(self, request):
        """
        Edits a classroom
        @param: WSGI Request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            classroom_id = data.get("classroom_id" , "")
            if not classroom_id:
                raise Exception("Classroom id not provided")
            classroom = ClassroomService().get(id=classroom_id, state=State.active())
            if not classroom:
                raise Exception("Classroom not found")
            name = str(data.get("name", "")).title().strip()
            if not name:
                raise Exception("Name not provided")
            if ClassroomService().filter(name=name, school=classroom.school, state=State.active()):
                raise Exception("Classroom already exists")
            classroom = ClassroomService().update(pk=classroom.id, name=name)
            if not classroom:
                raise Exception("Classroom not edited")
            return JsonResponse({"code": "100.000.000", "message": "Classroom edited successfully"})
        except Exception as e:
            lgr.exception("Edit classroom exception: %s" % e)
            return JsonResponse({
                "code": "999.999.999", "message": "Edit classroom failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def delete_classroom(self, request):
        """
        Deletes a classroom
        @param: WSGI Request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            classroom_id = data.get("classroom_id", "")
            if not classroom_id:
                raise Exception("Classroom id not provided")
            classroom = ClassroomService().get(id=classroom_id, state=State.active())
            if not classroom:
                raise Exception("Classroom not found")
            if UserService().filter(classroom=classroom, state=State.active()):
                raise Exception("Classroom can not be deleted: Students assigned to the classroom")
            classroom.delete()
            return JsonResponse({"code": "100.000.000", "message": "Classroom deleted successfully"})
        except Exception as e:
            lgr.exception("Delete classroom exception: %s" % e)
            return JsonResponse({
                "code": "999.999.999", "message": "Delete classroom failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_classrooms(self, request):
        """
        Fetches classrooms
        @param: WSGI Request
        @return: Success message and classrooms data or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            school_id = data.get("school_id", "")
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(code=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            classrooms_data = ClassroomService().filter(school=school, state=State.active()).values("id", "name")
            classrooms_data = list(classrooms_data)
            return JsonResponse({
                "code": "100.000.000", "message": "Classrooms fetched successfully", "data": classrooms_data})
        except Exception as e:
            lgr.exception("Get classrooms exception: %s" % e)
            return JsonResponse({
                "code": "999.999.999", "message": "Get classrooms failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_schools(self, request):
        """
        Fetches schools
        @param: WSGI Request
        @return: Success message and schools data or error message
        @rtype: JsonResponse
        """
        try:
            data = list(SchoolService().filter(state=State.active()).values("id", "name", "code"))
            return JsonResponse({"code": "100.000.000", "message": "Schools fetched successfully", "data": data})
        except Exception as e:
            lgr.exception("Get schools exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get schools failed with an exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_subjects(self, request):
        """
        Fetches subjects
        @param: WSGI Request
        @return: Success message and subjects data or error message
        @rtype: JsonResponse
        """
        try:
            data = list(SubjectService().filter(state=State.active()).values("name"))
            return JsonResponse({"code": "100.000.000", "message": "Subjects fetched successfully", "data": data})
        except Exception as e:
            lgr.exception("Get subjects exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get subjects failed with an exception", "error": e})

