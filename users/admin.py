from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import Role, Permission, RolePermission, User, StudentClassroom

admin.site.unregister(Group)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name',)

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
	list_display = ('role', 'permission', 'state', 'date_modified', 'date_created')
	search_fields = ('role__name', 'permission__name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = (
		'username', 'role', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'id',
		'is_superuser', 'state', 'date_modified', 'date_created'
	)
	list_filter = ('gender', 'is_superuser', 'role', 'date_created')
	search_fields = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'role__name', 'id',
		'reg_no', 'state__name'
	)
	fieldsets = (
		(
			'User Details', {
				'fields': ('username', 'email', 'phone_number', 'id', 'reg_no')
			}),
		('Other Info', {'fields': ('first_name', 'last_name', 'other_name', 'gender')}),
		('Status', {'fields': ('state', 'is_superuser', 'is_staff', 'is_active')}),
	)

@admin.register(StudentClassroom)
class StudentClassroomAdmin(admin.ModelAdmin):
	list_display = ('student', 'classroom', 'state', 'date_modified', 'date_created')
	search_fields = (
		'student__id', 'student__first_name', 'student__last_name', 'student__reg_no', 'classroom__name',
		'classroom__id', 'classroom__school__id', 'classroom__school__name', 'classroom__school__code', 'state__name'
	)
