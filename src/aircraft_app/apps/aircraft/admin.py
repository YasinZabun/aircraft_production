from django.contrib import admin
from .models import Aircraft

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('model', 'wing', 'fuselage', 'tail', 'avionics', 'assembled_at')
    list_filter = ('model',)
    search_fields = ('model',)
