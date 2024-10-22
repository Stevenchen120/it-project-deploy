from django.urls import path, include
from rest_framework.routers import DefaultRouter
from history.views import HistoryViewSet
from comments.views import CommentViewSet
from feedback.views import FeedbackViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'history', HistoryViewSet)
# Manually specify basename
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),  # JWT 路由
]
