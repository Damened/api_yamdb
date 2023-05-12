from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework import status, viewsets, filters, permissions
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import MethodNotAllowed

from .filters import TitleFilter
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          GetTitleSerializer,
                          ReviewSerializer,
                          TitleSerializer,)
from api.permissions import (IsAdminModeratorAuthorPermission,
                             IsAdminOrReadOnlyPermission,
                             IsAdministator)
from api.serializers import (SignUpUserSerializer,
                             GetJwtTokenSerializer,
                             UserSerializer,
                             NotAdminSerializer)
from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Review, Title, Category, Genre, Title
from users.models import User


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''Вьюсет для CRUD операций с коментариями.'''
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        '''Получаем все отзывы к произведению.'''
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        '''Переопределенный метод создания отзыва.'''
        serializer.save(author=self.request.user,
                        title=get_object_or_404(
                            Title, pk=self.kwargs.get("title_id")))


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для CRUD операций с комментариями.'''
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        '''Получаем все комментарии к посту.'''
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, pk=review_id,
                                   title__pk=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        '''Переопределенный метод создания отзыва.'''
        serializer.save(author=self.request.user,
                        review=get_object_or_404(
                            Review, pk=self.kwargs.get("review_id")))


def get_tokens_for_user(user):
    '''Обновляем пару токенов для пользователя.'''
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
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        current_user, _ = User.objects.get_or_create(
            email=email, username=username)
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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Функция получения токена"""
    serializer = GetJwtTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data.get('username')
    current_user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(
            current_user, confirmation_code):
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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT' or not request.user.is_admin:
            raise MethodNotAllowed(request.method)
        return super().update(request, *args, **kwargs)
