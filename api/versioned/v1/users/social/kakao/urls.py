from django.urls import path
from .views import KaKaoHealthCheckViewSet

urlpatterns = [
    path('health-check', KaKaoHealthCheckViewSet.as_view({'get': 'get_status'}))
]
