from django.shortcuts import render

# Create your views here.
# feedback_app/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    处理反馈的 CRUD 操作。
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        根据 URL 中的 `historical_figure` 查询参数过滤反馈。
        """
        historical_figure_id = self.request.query_params.get(
            'historical_figure')
        if historical_figure_id:
            return Feedback.objects.filter(
                historical_figure_id=historical_figure_id
            ).select_related('user', 'historical_figure').order_by('-created_at')
        return Feedback.objects.all().select_related('user', 'historical_figure').order_by('-created_at')

    def perform_create(self, serializer):
        """
        将反馈与当前用户关联。
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        覆盖 destroy 方法，确保只有反馈的作者可以删除自己的反馈。
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to delete this feedback.'},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
