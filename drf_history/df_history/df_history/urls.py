# df_history/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from history.views import HistoryViewSet
from comments.views import CommentViewSet
from feedback.views import FeedbackViewSet

router = DefaultRouter()
router.register(r'history', HistoryViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('api/', include('feedback.urls')),

]
