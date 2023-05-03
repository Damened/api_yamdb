import datetime
from rest_framework import serializers
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
    '''Сериализатор модели Review.'''
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
