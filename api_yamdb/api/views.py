from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets 
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError

from reviews.models import Comment, Review, Title, Category, Genre, Title

from .serializers import (CommentSerializer, 
                          ReviewSerializer,) 

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

from users.permissions import IsAdminModeratorAuthorPermission


class CategoryViewSet(viewsets.ModelViewSet): #ReadOnlyModelViewSet
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet): #ReadOnlyModelViewSet
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet): #ReadOnlyModelViewSet
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)

class ReviewViewSet(viewsets.ModelViewSet): 
    '''Вьюсет для CRUD операций с коментариями.''' 
    serializer_class = ReviewSerializer 
    permission_classes = (IsAdminModeratorAuthorPermission,) #(permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_obj_title(self): 
        '''Получение объекта произведения через его id в аргументе.''' 
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id")) 
        return title 

    def get_queryset(self): 
        '''Получаем все отзывы к произведению через метод get_obj_title.''' 
        new_queryset = self.get_obj_title().reviews.all() 
        return new_queryset 

    def perform_create(self, serializer): 
        '''Переопределенный метод создания отзыва. 
        Отзыв создается для объекта Title полученному через метод 
        get_obj_title.''' 
        # if Review.objects.filter( #
        # author=self.request.user, title=self.get_obj_title()).exists(): #
        #      raise ValidationError('Нельзя оставить отзыв дважды к одному произведению.') #
        serializer.save(author=self.request.user, title=self.get_obj_title())

class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для CRUD операций с комментариями.''' 
    serializer_class = CommentSerializer 
    permission_classes = (IsAdminModeratorAuthorPermission,) #(permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_obj_review(self): 
        '''Получение объекта Отзыв через его id в аргументе.''' 
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id")) 
        return review 

    def get_queryset(self): 
        '''Получаем все комментарии к посту.
        Используем id отзыва и id произведения.''' 
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, pk=review_id,
                                   title__pk=title_id)
        return review.comments.all()  

    def perform_create(self, serializer): 
        '''Переопределенный метод создания отзыва. 
        Отзыв создается для объекта Title полученному через метод 
        get_obj_rewiew.''' 
        serializer.save(author=self.request.user, review=self.get_obj_review())