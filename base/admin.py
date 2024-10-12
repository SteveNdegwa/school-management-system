from django.contrib import admin

from base.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)

