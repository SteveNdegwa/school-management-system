from django.contrib import admin

from base.models import State, TransactionType, Transaction, NotificationType, Notification, School, Class, Subject


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = (
		'transaction_type', 'source_ip', 'request', 'response', 'notification_response', 'state', 'date_modified',
		'date_created')
	search_fields = ('transaction_type__name', 'source_ip', 'state')

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = (
		'notification_type', 'title', 'message', 'destination', 'state', 'date_modified', 'date_created')
	search_fields = ('notification_type__name', 'title', 'message', 'destination', 'state')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'state', 'date_modified', 'date_created')
	search_fields = ('code', 'name', 'state__name')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
	list_display = ('name', 'school', 'state', 'date_modified', 'date_created')
	search_fields = ('school__name', 'school__code', 'name', 'state__name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')

