from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/signup/', UserCreate.as_view(), name="create_user"),
    path('users/<int:pk>/', UserDetail.as_view(), name="get_user_details"),
]