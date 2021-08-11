import re

from django.contrib.auth.backends import ModelBackend

from BackApis.models import Users


def get_user_by_account_name(account):
    """
    通过账号获取用户模型对象
    :param account: mobile / username
    :return: user or None
    """
    try:
        user = Users.objects.get(username=account)
        return user
    except Users.DoesNotExist:
        return None


def get_user_by_account_phone(account):
    try:
        if re.match(r'1[3-9]\d{9}', account):
            user = Users.objects.get(phone=account)
            print('user phone', user, str(user))
            return user
    except Users.DoesNotExist:
        return None


class UsernameMobileAuthBackend(ModelBackend):
    """自定义认证后端类实现多账号登录"""

    def authenticate(self, request, username=None, phone=None, password=None, **kwargs):
        if username:
            # 1.根据用户名或手机号 查询user
            user = get_user_by_account_name(username)
            # 2.校验用户密码
            if user and user.check_password(password) and user.is_active:
                # 3.返回user or None
                return user
        elif phone:
            # 1.根据用户名或手机号 查询user
            user = get_user_by_account_phone(phone)
            # 2.校验用户密码
            if user and user.check_password(password) and user.is_active:
                # 3.返回user or None
                return user
