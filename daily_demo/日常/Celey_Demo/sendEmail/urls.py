from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('register', RegisterViewsSet)

urlpatterns = [
    path(r'', include(router.urls)),
    # 自定义的jwt认证
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
