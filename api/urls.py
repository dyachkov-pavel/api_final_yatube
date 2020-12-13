from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIGroup, APIFollow, PostViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

router_posts_v1 = DefaultRouter()
router_posts_v1.register('posts', PostViewSet, basename='post-list')
router_posts_v1.register(r'posts/(?P<post_id>.+)/comments', CommentViewSet, basename='comment-list')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router_posts_v1.urls)),
    path('v1/group/', APIGroup.as_view()),
    path('v1/follow/', APIFollow.as_view()),
]
