from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView
)
from .views import (
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
    PostViewSet,
    UserCreateViewSet,
    LogoutViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follows')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
router.register('auth/signup', UserCreateViewSet, basename='auth-signup')
router.register('auth/logout', LogoutViewSet, basename='auth-logout')

urlpatterns = [
    path('v1/', include([
        path('', include(router.urls)),
        path('auth/login/', obtain_auth_token, name='login'),
        path('jwt/verify/', TokenVerifyView.as_view(), name='token-verify'),
        path('jwt/create/', TokenObtainPairView.as_view(), name='token-create'),
        path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    ])),
]