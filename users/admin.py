from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import Role, Permission, RolePermission, User, Student, Teacher

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
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'is_superuser', 'role',
        'state', 'date_modified', 'date_created')
	list_filter = ('gender', 'is_superuser', 'role', 'date_created')
	search_fields = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'state__name')
	fieldsets = (
		(
			'User Details', {
				'fields': ('username', 'email', 'phone_number')
			}),
		('Other Info', {'fields': ('first_name', 'last_name', 'other_name')}),
		('Status', {'fields': ('state', 'is_superuser', 'is_staff', 'is_active')}),
	)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		return super().get_queryset(request).filter(role=Role.student())
	list_display = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'state',
		'date_modified', 'date_created')
	list_filter = ('gender', 'date_created')
	search_fields = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'state__name')
	fieldsets = (
		(
			'User Details', {
				'fields': ('username', 'email', 'phone_number')
			}),
		('Other Info', {'fields': ('first_name', 'last_name', 'other_name')}),
		('Status', {'fields': ('state',)}),
	)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		return super().get_queryset(request).filter(role=Role.teacher())
	list_display = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'state',
		'date_modified', 'date_created')
	list_filter = ('gender', 'date_created')
	search_fields = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'state__name')
	fieldsets = (
		(
			'User Details', {
				'fields': (('username', 'email', 'phone_number'),)
			}),
		('Other Info', {'fields': ('first_name', 'last_name', 'other_name')}),
		('Status', {'fields': ('state',)}),
	)