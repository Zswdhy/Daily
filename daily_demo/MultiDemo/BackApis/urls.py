from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from BackApis import views
from BackApis.views import UsersViewSet

router = DefaultRouter()
router.register('register', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('', include(router.urls)),
    path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
