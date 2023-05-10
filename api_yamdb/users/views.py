from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL
from .models import User
from .permissions import IsAdministator
from users.serializers import (SignUpUserSerializer,
                               GetJwtTokenSerializer,
                               UserSerializer,
                               NotAdminSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up_user(request):
    '''Функция регистрации пользователей'''
    serializer = SignUpUserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            current_user, _ = User.objects.get_or_create(
                email=email, username=username,)
        except IntegrityError:
            raise serializers.ValidationError(
                'Такой пользователь уже существует')
        confirm_code = default_token_generator.make_token(current_user)
        send_mail('Confirmation of registration',
                  f'your code: {confirm_code}',
                  ADMIN_EMAIL,
                  [email],
                  fail_silently=False,)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Функция получения токена"""
    serializer = GetJwtTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        return Response(
            {'error': 'Такого пользователя не существует.'},
            status=status.HTTP_404_NOT_FOUND)
    if data.get('confirmation_code') == user.confirmation_code:
        token = RefreshToken.for_user(user).access_token
        return Response(
            {'token': str(token)},
            status=status.HTTP_201_CREATED)
    return Response(
        {'error': 'Неверный код подтверждения.'},
        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdministator,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
