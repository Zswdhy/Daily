from rest_framework import serializers

from BackApis.models import Users


class UsersSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = Users
        fields = ['username', 'password', 'email', 'phone']
