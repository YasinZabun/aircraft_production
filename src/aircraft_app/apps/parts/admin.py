from django.contrib import admin
from .models import Part

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_type', 'aircraft_model', 'team', 'stock')
    list_filter = ('aircraft_model', 'part_type', 'team')
    search_fields = ('part_type', 'aircraft_model', 'team__name')
