import re
from rest_framework import serializers


def validate_username(value):
    '''Запрещает пользователям присваивать себе имя me.
    Запрещает использовать недопустимые символы.'''
    regex = re.sub(r'^[\w.@+-]+$', '', value)
    if value in regex:
        raise serializers.ValidationError(
            f'Имя пользователя не должно содержать {regex}')
    elif value.lower() == 'me':
        raise serializers.ValidationError(
            'Использовать имя "me" запрещено')
    return value


def validate_score(value):
    '''Проверяет чтобы score было от 1 до 10.
    Работает для админки.'''
    if 0 > value or value > 10:
        raise serializers.ValidationError(
            'Оценка должна быть в деапазоне от 1 до 10')
    return value
