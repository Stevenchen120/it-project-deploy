# comments/models.py
from django.db import models
from django.contrib.auth.models import User
from history.models import HistoricalFigure  # Ensure this model exists


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    historical_figure = models.ForeignKey(
        HistoricalFigure, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.historical_figure}"

class Like(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='likes')
    comment = models.ForeignKey(
    Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can like a comment only once
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} liked Comment {self.comment.id}"

