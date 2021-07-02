# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


def Hello(request):
    return HttpResponse('ok')


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teachers.objects.all()
    # 局部引入多个过滤类后端，无须在 settings 中配置全局设置
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('gender', 'name')
    search_fields = ('name',)
    ordering_fields = ('age', 'gender')

    authentication_classes = []
    permission_classes = []
    # throttle_classes = [] # 访问限制


class Test(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        name = request.GET.get('name')
        if name:
            return Response(name)
        else:
            return Response('不存在')


class QuerySetApiTestModelViewSet(viewsets.ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = []
    permission_classes = []

    def list(self, request, *args, **kwargs):
        # id , name ,gender , age
        test1 = Teachers.objects.values_list('id', 'name', 'gender', 'age')
        print(test1, type(test1))

        from django.db.models.aggregates import Count
        # 分组
        test2 = Teachers.objects.annotate(count=Count('age'))
        for item in test2:
            print(item)
        print('2', test2, test2.count)
        # 聚合
        test3 = Teachers.objects.aggregate()

        return Response('data')
