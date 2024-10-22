from django.contrib import admin
from .models import HistoricalFigure
# Register your models here.
admin.site.register(HistoricalFigure)
class HistoricalFigureAdmin(admin.ModelAdmin):
    list_display = ('given_names', 'family_name', 'birth_year', 'death_year')