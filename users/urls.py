from django.urls import re_path

from users.views import UsersAdministration

urlpatterns = [
    re_path(r'create-super-admin/$', UsersAdministration().create_super_admin),
    re_path(r'create-admin/$', UsersAdministration().create_admin),
    re_path(r'create-clerk/$', UsersAdministration().create_clerk),
    re_path(r'create-student/$', UsersAdministration().create_student),
    re_path(r'edit-user/$', UsersAdministration().edit_user),
    re_path(r'get-user/$', UsersAdministration().get_user),
    re_path(r'filter-users/$', UsersAdministration().filter_users),
    re_path(r'search-users/$', UsersAdministration().search_users),
]