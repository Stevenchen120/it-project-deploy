# comments/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Comment, Like
from .serializers import CommentSerializer, LikeSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限类，仅允许评论的作者编辑或删除评论。
    """

    def has_object_permission(self, request, view, obj):
        # 安全方法（GET, HEAD, OPTIONS）允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 非安全方法（PUT, DELETE 等）仅允许评论作者
        return obj.author == request.user


class CommentViewSet(viewsets.ModelViewSet):
    """
    处理评论的 CRUD 操作及自定义动作（如点赞和取消点赞）。
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        可选：根据 URL 中的 `historical_figure` 查询参数过滤返回的评论。
        """
        historical_figure_id = self.request.query_params.get(
            'historical_figure')
        if historical_figure_id:
            return Comment.objects.filter(
                historical_figure_id=historical_figure_id
            ).select_related('parent', 'author').prefetch_related('replies', 'likes')
        return Comment.objects.all().select_related('parent', 'author').prefetch_related('replies', 'likes')

    def perform_create(self, serializer):
        """
        将评论与当前用户关联，并可选地与父评论关联。
        """
        parent_id = self.request.data.get('parent')
        parent_comment = Comment.objects.get(
            id=parent_id) if parent_id else None
        serializer.save(author=self.request.user, parent=parent_comment)

    def get_permissions(self):
        """
        根据动作分配不同的权限。
        """
        if self.action in ['like', 'unlike', 'liked_by_user']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        自定义动作：点赞评论。确保用户只能点赞一次。
        """
        user = request.user
        comment = self.get_object()

        # 检查用户是否已点赞
        if Like.objects.filter(user=user, comment=comment).exists():
            return Response({'detail': 'You have already liked this comment.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 添加点赞
        Like.objects.create(user=user, comment=comment)

        # 返回更新后的点赞数
        likes_count = Like.objects.filter(comment=comment).count()
        return Response({'likes_count': likes_count}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        自定义动作：取消点赞评论。允许用户移除自己的点赞。
        """
        user = request.user
        comment = self.get_object()

        # 尝试找到点赞实例
        try:
            like = Like.objects.get(user=user, comment=comment)
            like.delete()
            likes_count = Like.objects.filter(comment=comment).count()
            return Response({'likes_count': likes_count}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this comment.'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def liked_by_user(self, request, pk=None):
        """
        检查当前用户是否已点赞特定评论。
        """
        comment = self.get_object()
        user = request.user
        liked = Like.objects.filter(user=user, comment=comment).exists()
        return Response({'liked': liked}, status=status.HTTP_200_OK)
