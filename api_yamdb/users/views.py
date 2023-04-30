from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .permissions import IsAdministator
from users.serializers import (SignUpUserSerializer,
                               GetJwtTokenSerializer,
                               UserSerializer)

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


@permission_classes([permissions.IsAuthenticated, IsAdministator])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']

    def get_object(self):
        username = self.kwargs.get('username')

        if username == 'me' and (self.request.method == 'GET' or
                                 self.request.method == 'PATCH'):
            return self.request.user

        current_user = get_object_or_404(User, username=username)
        return current_user
