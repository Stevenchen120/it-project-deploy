

from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'historical_figure',
                    'rating', 'created_at')
    search_fields = ('title', 'user__username',
                     'historical_figure__given_names', 'historical_figure__family_name')
    list_filter = ('rating', 'created_at')
