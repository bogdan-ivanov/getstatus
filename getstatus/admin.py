from django.contrib import admin

from .models import System, Incident


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    pass


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('system', 'start', 'end')
