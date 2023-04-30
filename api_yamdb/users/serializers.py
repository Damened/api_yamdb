from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name', 'bio', 'role'


class SignUpUserSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователей"""
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, data):
        """Запрещает пользователям повторно использовать
        username и email."""
        current_username = data.get('username')
        current_email = data.get('email')
        if User.objects.filter(
            username=current_username,
            email=current_email
        ).exists():
            return data
        elif User.objects.filter(username=current_username).exists():
            raise serializers.ValidationError(
                'Данное имя пользователя уже занято!'
            )
        elif User.objects.filter(email=current_email).exists():
            raise serializers.ValidationError(
                'Данный Email уже занят!'
            )
        return data

    def validate_username(self, value):
        """Запрещает пользователям присваивать себе имя me
        и использовать недопустимые символы."""
        regex = re.sub(r'^[\w.@+-]+$', '', value)
        if value in regex:
            raise serializers.ValidationError(
                f'Имя пользователя не должно содержать {regex}'
            )
        elif value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено'
            )
        return value


class GetJwtTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена"""
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()
