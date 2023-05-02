import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Comment, Review, Category, Genre, Title
# from .models import Category, Genre, Title
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
        fields = '__all__'
        read_only_fields = ('author', 'title')


class CommentSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Comment.'''
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Comment 
        fields = '__all__'
        read_only_fields = ('author', 'review')
