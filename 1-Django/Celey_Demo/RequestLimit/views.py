from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import SimpleRateThrottle


class LuffyAnonRateThrottle(SimpleRateThrottle):
    """
    匿名用户，根据IP进行限制
    """
    scope = "luffy_anon"

    def get_cache_key(self, request, view):
        # 用户已登录，则跳过 匿名频率限制
        if request.user:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class LuffyUserRateThrottle(SimpleRateThrottle):
    """
    登录用户，根据用户token限制
    """
    scope = "luffy_user"

    def get_ident(self, request):
        """
        认证成功时：request.user是用户对象；request.auth是token对象
        :param request:
        :return:
        """
        # return request.auth.token
        return "user_token"

    def get_cache_key(self, request, view):
        """
        获取缓存key
        :param request:
        :param view:
        :return:
        """
        # 未登录用户，则跳过 Token限制
        if not request.user:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class TestView(APIView):
    throttle_classes = [LuffyUserRateThrottle, LuffyAnonRateThrottle, ]

    def get(self, request, *args, **kwargs):
        # self.dispatch
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')


def TestParams(request):
    name = request.GET.get('name')
    if name:
        return HttpResponse(f'name:{name}存在')
    else:
        return HttpResponse(f'name不存在')
