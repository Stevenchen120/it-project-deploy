# feedback_app/serializers.py

from rest_framework import serializers
from .models import Feedback
from history.models import HistoricalFigure
from django.contrib.auth.models import User


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    historical_figure = serializers.PrimaryKeyRelatedField(
        queryset=HistoricalFigure.objects.all())

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_id', 'historical_figure',
                  'title', 'message', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'user_id', 'created_at']
