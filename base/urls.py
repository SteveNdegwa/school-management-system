from django.urls import re_path

from base.views import BaseAdministration

urlpatterns = [
    re_path(r'create-classroom/$', BaseAdministration().create_classroom),
    re_path(r'edit-classroom/$', BaseAdministration().edit_classroom),
    re_path(r'delete-classroom/$', BaseAdministration().delete_classroom),
    re_path(r'get-classrooms/$', BaseAdministration().get_classrooms),
    re_path(r'get-schools/$', BaseAdministration().get_schools),
    re_path(r'get-subjects/$', BaseAdministration().get_subjects),
]