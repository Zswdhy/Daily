from django.conf import settings
import random
from django.core.mail import send_mail


def random_str(length=6):
    random_string = ''
    chars = '0123456789'
    lengths = len(chars) - 1
    for i in range(length):
        random_string += chars[random.randint(0, lengths)]
    return random_string


def send_email(user, email, random_string):
    subject = f'当前用户：{user}，系统生成的验证码为【{random_string}】'
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    send_mail('注册验证码', subject, from_email, [to_email, ], fail_silently=False)


def jwt_response_payload_handler(token, user, request=None):
    # 在 settings 内修改 JWT_AUTH JWT_RESPONSE_PAYLOAD_HANDLER 的路由地址，即可以使用本地重写的方法
    # 在此 app 下 views 重新定义
    data = {
        'token': token,
        'name': str(user),
    }
    return data


def jwt_response_payload_error_handler():
    data = {
        "code": 400,
        "message": "用户名或者密码错误",
    }
    return data
