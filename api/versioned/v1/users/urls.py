from django.urls import path, re_path
from common.routers import CustomSimpleRouter
from .views import UserViewSet, UserLoginTokenViewSet, UserProfileOnwerViewSet, RefreshTokenViewSet

router = CustomSimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create'})),
    re_path(r'^(?P<pk>[0-9a-f-]+)$', UserViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
    path('login', UserLoginTokenViewSet.as_view({'post': 'create'})),
    path('logout', UserViewSet.as_view({'get': 'logout'})),
    path('profile', UserProfileOnwerViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'})),
    path('refresh_token', RefreshTokenViewSet.as_view({'post': 'partial_update'})),
]
urlpatterns += router.urls