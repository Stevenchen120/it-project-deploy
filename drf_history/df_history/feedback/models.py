

from django.db import models
from django.contrib.auth.models import User
from history.models import HistoricalFigure  # 确保导入正确的 HistoricalFigure 模型


class Feedback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feedbacks')
    historical_figure = models.ForeignKey(
        HistoricalFigure, on_delete=models.CASCADE, related_name='feedbacks')
    title = models.CharField(max_length=255)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # 评分（1-5）
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        ordering = ['-created_at']  # 按创建时间降序排列

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.historical_figure}"
