from rest_framework import serializers
import re


def validate_username(value):
    '''Запрещает пользователям присваивать себе имя me.
    Запрещает использовать недопустимые символы.'''
    if value == 'me':
        raise serializers.ValidationError(
            'Использовать имя "me" запрещено')
    regex = re.sub(r'^[\w.@+-]+$', '', value)
    if value in regex:
        raise serializers.ValidationError(
            f'Имя пользователя не должно содержать {regex}')
    return value
