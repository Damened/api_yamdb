from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Comment, Review, Title, User
# from users.models import User импорт из приложения


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.StringRelatedField(many=True, read_only=True)  # Строковое представление, может быть несколько жанров
    # Или нужно использовать вложенный сериализатор...
    category = serializers.StringRelatedField(many=False, read_only=True)  # Строковое представление

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)
        read_only_fields = ('rating',)
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        sum_score = 0
        for review in reviews:
            sum_score += review.score
        return sum_score // len(reviews)  # Сумма оценок делится на их количество без остатка

class ReviewSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Reviews.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Review 
        fields = ('__all__') 
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
        fields = ('__all__') 
        read_only_fields = ('author', 'review')
