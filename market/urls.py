from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'images', ImageViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'locations2', LocationRange)
router.register(r'listings', ListingViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/signup/', UserCreate.as_view(), name="create_user"),
    path('users/<int:pk>/', UserDetail.as_view(), name="get_user_details"),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('message_list/<int:sender_id>/<int:recipient_id>/', MessageList.as_view(), name='message_list'),
    path('chat_list/<int:user_id>/', UserChats.as_view(), name='user_chats'),
    path('review_fetch/<int:reviewer>/<int:seller>/', ReviewFetch.as_view(), name='review'),
]