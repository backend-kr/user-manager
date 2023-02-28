from django.urls import path, re_path
from common.routers import CustomSimpleRouter
from .views import UserViewSet, UserLoginTokenViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = CustomSimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create'})),
    re_path(r'^(?P<pk>[0-9a-f-]+)$', UserViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
    path('login', UserLoginTokenViewSet.as_view({'post': 'create'})),
    path('logout', UserViewSet.as_view({'get': 'logout'})),
]
urlpatterns += router.urls