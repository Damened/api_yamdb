from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets 
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, Title

from .serializers import (CommentSerializer, 
                          ReviewSerializer,) 

from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)

class ReviewViewSet(viewsets.ModelViewSet): 
    '''Вьюсет для CRUD операций с коментариями.''' 
    serializer_class = ReviewSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    def get_obj_title(self): 
        '''Получение объекта произведения через его id в аргументе.''' 
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id")) 
        return title 

    def get_queryset(self): 
        '''Получаем все коментарии к посту через метод get_obj_title.''' 
        new_queryset = self.get_obj_title().review.all() 
        return new_queryset 

    def perform_create(self, serializer): 
        '''Переопределенный метод создания отзыва. 
        Отзыв создается для объекта Title полученному через метод 
        get_obj_title.''' 
        serializer.save(author=self.request.user, title=self.get_obj_title())

class CommentViewSet(viewsets.ModelViewSet):
    pass
