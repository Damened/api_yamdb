import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)
        read_only_fields = ('rating',)
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        sum_score = 0
        if len(reviews) != 0:
            for review in reviews:
                sum_score += review.score
            return sum_score // len(reviews)  # Сумма оценок делится на их количество без остатка
        return sum_score

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError('Год выпуска произведения '
                                              'не может быть больше текущего')
        return value


class ReviewSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Reviews.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Review 
        fields = ('id', 'text', 'author', 'score', 'pub_date',) 
        read_only_fields = ('author', 'title')

    def validate_score(self, value):
        '''Валидатор поля score, его значение должно быть от 1 до 10.'''
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Comment.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Comment 
        fields = ('id', 'text', 'author', 'pub_date',) 
        read_only_fields = ('author', 'review')
