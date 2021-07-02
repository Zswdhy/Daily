from django.urls import path
from .views import *

urlpatterns = [
    path('limit/', TestView.as_view()),
    path('test/', TestParams),
]
