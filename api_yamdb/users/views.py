from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .permissions import IsAdministator
from users.serializers import (SignUpUserSerializer,
                               GetJwtTokenSerializer,
                               UserSerializer,
                               NotAdminSerializer)#

# Create your views here.
def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up_user(request):
    """Функция регистрации пользователей"""
    serializer = SignUpUserSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('username')
        email = request.data.get('email')

        current_user = User.objects.create_user(username=username, email=email)
        confirm_code = default_token_generator.make_token(current_user)
        send_mail('Confirmation of registration',
                  f'your code: {confirm_code}',
                  'yamdb@ya.ru',
                  [email],
                  fail_silently=False,)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Функция получения токена"""
    serializer = GetJwtTokenSerializer(data=request.data)
    if serializer.is_valid():
        current_user = get_object_or_404(
            User, username=request.data.get('username'))
        return Response(get_tokens_for_user(current_user))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
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
    
