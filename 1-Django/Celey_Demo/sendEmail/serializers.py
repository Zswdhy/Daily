from rest_framework import serializers
from .models import *
from Exception.my_validation_error import MyValidationError
from .utils import send_email


class UserModelSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(label='确认密码', write_only=True)
    check_code = serializers.CharField(label='验证码', write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'password', 'password_2', 'email', "check_code"]

    def validate(self, attrs):
        password = attrs['password']
        password_2 = attrs['password_2']
        if password != password_2:
            raise MyValidationError({'code': '400', 'message': '两次输入的密码不一致'})

        # yanzheng_code = random_str()
        yanzheng_code = '123456'
        print('随机验证码', yanzheng_code)
        # send_email(attrs['username'], attrs['email'], yanzheng_code)
        send_email(attrs['username'], attrs['email'], yanzheng_code)
        check_code = attrs['check_code']
        print('录入验证码', check_code)

        if yanzheng_code != check_code:
            raise MyValidationError({'code': '400', 'message': '验证码不正确'})

        return attrs

    def create(self, validated_data):
        print('data origin', validated_data)
        del validated_data['check_code']
        del validated_data['password_2']
        # 明文
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()

        return user
