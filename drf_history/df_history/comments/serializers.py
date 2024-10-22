# comments/serializers.py

from rest_framework import serializers
from .models import Comment, Like, HistoricalFigure
from django.contrib.auth.models import User


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    historical_figure = serializers.PrimaryKeyRelatedField(
        queryset=HistoricalFigure.objects.all())
    replies = RecursiveField(many=True, required=False, read_only=True)
    likes_count = serializers.IntegerField(
        source='likes.count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_id', 'text', 'created_at',
                  'historical_figure', 'replies', 'parent', 'likes_count']
        read_only_fields = ['id', 'author',
                            'author_id', 'created_at', 'likes_count']
