from rest_framework import serializers
from .models import HistoricalFigure
# class HistoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HistoricalFigure
#         fields = '__all__'

# class HistoryDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HistoricalFigure
#         fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalFigure
        fields = '__all__'
