from rest_framework import serializers
from .models import *
from Exception.my_validation_error import MyValidationError


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'

    def validate(self, attrs):
        print('attrs', attrs)
        id = attrs['id']
        if Teachers.objects.filter(id=id):
            raise MyValidationError({'code': '400', 'message': '此id已经存在，请勿重新录入系统'})
        return attrs

    def create(self, validated_data):
        user = Teachers(**validated_data)
        user.save()
        return user
