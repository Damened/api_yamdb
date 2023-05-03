import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, Category, Genre, Title, GenreTitle

from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)
        read_only_fields = ('rating',)
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        category = validated_data.pop('category')
        currents_genres = []
        for genre in genres:
            currents_genres.append(Genre.objects.get(slug=genre))
        validated_data.append(currents_genres)
        current_category = Category.objects.get(slug=category)
        validated_data.append(current_category)
        title = Title.objects.create(**validated_data)
        for genre in currents_genres:
            GenreTitle.objects.create(
                genre=genre,
                title=title,
            )

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
    
    # def validate(self, data):
    #     request = self.context['request']
    #     author = request.user
    #     title_id = self.context.get('view').kwargs.get('title_id')
    #     title = get_object_or_404(Title, pk=title_id)
    #     if (
    #         request.method == 'POST'
    #         and Review.objects.filter(title=title, author=author).exists()
    #     ):
    #         raise serializers.ValidationError('Может существовать только один отзыв!')
    #     return data
    
  


class CommentSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Comment.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Comment 
        fields = ('id', 'text', 'author', 'pub_date',) 
        read_only_fields = ('author', 'review')
