from rest_framework import viewsets

from BackApis.models import Users
from BackApis.serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
