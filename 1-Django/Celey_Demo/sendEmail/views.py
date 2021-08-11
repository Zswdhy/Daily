from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView, ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from .utils import jwt_response_payload_handler, jwt_response_payload_error_handler
import jwt
from django.http import HttpRequest, JsonResponse
import datetime
from django.conf import settings
from .models import Users


# 自定义 JWT token 认证  装饰器使用
def auth(view_func):
    def wrapper(request: HttpRequest):
        token = request.META.get('HTTP_AUTHORIZATION', None)  # 拿到http_jwt 字典的值
        if not token:  # 认证失败
            return JsonResponse({'code': '400', 'message': 'Token 认证失败'})
        key = settings.SECRET_KEY
        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, key, algorithms=['HS256'])  # 解失败，被改过；接成功；没改过；
            user = Users.objects.filter(pk=payload['user_id']).first()  # 查询一次数据库；
            if user:  # 拿到user,
                request.user = user  # request 动态添加属性；
                ret = view_func(request)
                return ret
            else:
                return JsonResponse({'code': 400, 'message': '用户名或密码错误'})
        except jwt.ExpiredSignatureError as e:
            return JsonResponse({'code': 400, 'message': 'jwt 过期', 'error': str(e)})
        except Exception as e:
            return JsonResponse({'code': 400, 'message': '用户名或密码错误', 'error': str(e)})

    return wrapper


class MyJSONWebTokenAPIView(JSONWebTokenAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                response_data.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                         token, expires=expiration, httponly=True)
            return Response(response_data)
        error_data = jwt_response_payload_error_handler()
        return Response(error_data)


class MyObtainJSONWebToken(ObtainJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyRefreshJSONWebToken(RefreshJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyVerifyJSONWebToken(VerifyJSONWebToken, MyJSONWebTokenAPIView):
    pass


obtain_jwt_token = MyObtainJSONWebToken.as_view()
refresh_jwt_token = MyRefreshJSONWebToken.as_view()
verify_jwt_token = MyVerifyJSONWebToken.as_view()


class RegisterViewsSet(viewsets.ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = Users.objects.all()
    authentication_classes = []
    permission_classes = []
