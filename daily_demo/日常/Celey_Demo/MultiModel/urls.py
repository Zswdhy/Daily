from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet)
router.register('querysetTest', QuerySetApiTestModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hellotest/', Hello, name='hello'),
    path('test/', Test.as_view(), name='test'),
]
