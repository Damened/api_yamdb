import re
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class NotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        read_only_fields = ('role',)


class SignUpUserSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователей"""
    username = serializers.CharField(
        max_length=150,
        required=True,)
    email = serializers.EmailField(
        max_length=254,
        required=True,)

    def validate_username(self, value):
        '''Запрещает пользователям присваивать себе имя me.
        Запрещает использовать недопустимые символы.'''
        regex = re.sub(r'^[\w.@+-]+$', '', value)
        if value in regex:
            raise serializers.ValidationError(
                f'Имя пользователя не должно содержать {regex}')
        elif value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено')
        return value


class GetJwtTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена"""
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()
