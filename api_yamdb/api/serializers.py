from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError

from reviews.models import Category, Genre, Comment, Review, Title

# from users.models import User импорт из приложения


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
    genre = GenreSerializer(many=True, read_only=True)  # Строковое представление, может быть несколько жанров
    # Или нужно использовать вложенный сериализатор...
    # category = serializers.StringRelatedField(many=False, read_only=True)  # Строковое представление
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)
        read_only_fields = ('rating',)
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        sum_score = 0
        if len(reviews) != 0: # добавил условие чтобы избежать деления на ноль при добавлении произведения
           for review in reviews:
               sum_score += review.score
           return sum_score // len(reviews)  # Сумма оценок делится на их количество без остатка
        return sum_score # добавил 

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
        if 0 > value or value > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value
    
    # def validate(self, data):
    # #     '''Валидатор количества отзывов текущего юзера у произведения.'''
    # #     if Review.objects.filter( # title = get_object_or_404(Title, pk=self.kwargs.get("title_id")) 
    # #     author=self.context['request'].user, title=self.context['request'].title.exists()) : #
    # #         raise ValidationError('Нельзя оставить отзыв дважды к одному произведению.') #
    # # # user = self.context['request'].user
    #     return (self.context, data)

class CommentSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Comment.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Comment 
        fields = ('id', 'text', 'author', 'pub_date',) 
        read_only_fields = ('author', 'review')
