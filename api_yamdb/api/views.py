from rest_framework import viewsets 
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, Title

from .serializers import (CommentSerializer, 
                          ReviewSerializer,) 

class ReviewViewSet(viewsets.ModelViewSet): 
    '''Вьюсет для CRUD операций с озывами.''' 
    serializer_class = ReviewSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    def get_obj_title(self): 
        '''Получение объекта Произведения через его id в аргументе.''' 
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id")) 
        return title 

    def get_queryset(self): 
        '''Получаем все отзывы к произведению через метод get_obj_title.''' 
        new_queryset = self.get_obj_title().review.all() 
        return new_queryset 

    def perform_create(self, serializer): 
        '''Переопределенный метод создания отзыва. 
        Отзыв создается для объекта Title полученному через метод 
        get_obj_title.''' 
        serializer.save(author=self.request.user, title=self.get_obj_title())

class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для CRUD операций с комментариями.''' 
    serializer_class = CommentSerializer 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    def get_obj_rewiew(self): 
        '''Получение объекта Отзыв через его id в аргументе.''' 
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id")) 
        return review 

    def get_queryset(self): 
        '''Получаем все комментарии к посту через метод get_obj_rewiew.''' 
        new_queryset = self.get_obj_rewiew().comments.all() 
        return new_queryset 

    def perform_create(self, serializer): 
        '''Переопределенный метод создания отзыва. 
        Отзыв создается для объекта Title полученному через метод 
        get_obj_rewiew.''' 
        serializer.save(author=self.request.user, review=self.get_obj_rewiew())