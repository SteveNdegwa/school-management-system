from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import Role, Permission, RolePermission, User

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
		'username', 'role', 'school', 'classroom',  'first_name', 'last_name', 'gender', 'email', 'phone_number',
		'id_no', 'state', 'date_modified', 'date_created'
	)
	list_filter = ('role', 'school', 'classroom', 'gender', 'date_created')
	search_fields = (
		'username', 'first_name', 'last_name', 'other_name', 'gender', 'email', 'phone_number', 'school__name',
		'school__id', 'school__code', 'classroom__id', 'classroom__name', 'role__name', 'id_no', 'reg_no', 'state__name'
	)
	fieldsets = (
		('User Details', {'fields': ('username', 'email', 'phone_number', 'other_phone_number', 'id_no', 'reg_no')}),
		('Important Info', {'fields': ('role', 'school', 'classroom')}),
		('Other Info', {'fields': ('first_name', 'last_name', 'other_name', 'gender')}),
		('Status', {'fields': ('state', 'is_superuser', 'is_staff', 'is_active')}),
	)
