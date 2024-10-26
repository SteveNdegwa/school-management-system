from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import Role, Permission, RolePermission, User, StudentProfile, TeacherProfile, Guardian

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

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
	list_display = (
		'first_name', 'last_name', 'other_name', 'gender', 'id_no', 'email', 'phone_number', 'other_phone_number',
		'state', 'date_modified', 'date_created')
	list_filter = ('gender', 'date_created')
	search_fields = (
		'first_name', 'last_name', 'other_name', 'id_no', 'gender', 'email', 'phone_number', 'other_phone_number',
		'state__name')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ('student', 'student_id', 'guardian', 'other_guardian', 'state', 'date_modified', 'date_created')
	search_fields = (
		'student__first_name', 'student__last_name', 'student__other_name', 'student_id', 'guardian__id',
		'other_guardian__id', 'state__name')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
	list_display = (
		'teacher', 'teacher_id', 'id_no', 'tsc_no', 'other_phone_number', 'state', 'date_modified', 'date_created')
	search_fields = (
		'teacher__first_name', 'teacher__last_name', 'teacher__other_name', 'teacher_id', 'id_no', 'tsc_no',
		'other_phone_number','state__name')
