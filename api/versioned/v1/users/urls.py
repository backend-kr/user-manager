from django.urls import path, re_path, include
from common.routers import CustomSimpleRouter
from .views import UserViewSet, UserLoginTokenViewSet, UserProfileOnwerViewSet, RefreshTokenViewSet
from .social.urls import urlpatterns as social_urlpatterns

router = CustomSimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create', 'put': 'partial_update', 'delete': 'destroy'})),
    path('health_check', UserViewSet.as_view({'get': 'health_check'})),
    path('login', UserLoginTokenViewSet.as_view({'post': 'create'})),
    path('logout', UserViewSet.as_view({'get': 'logout'})),
    path('profile', UserProfileOnwerViewSet.as_view({'get': 'retrieve'})),
    path('refresh_token', RefreshTokenViewSet.as_view({'post': 'partial_update'})),
    path('social', include(social_urlpatterns))
]
urlpatterns += router.urls