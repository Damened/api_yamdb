from django.shortcuts import get_object_or_404

from rest_framework import serializers

from api.validators import validate_username
from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class NotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        read_only_fields = ('role',)


class SignUpUserSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователей"""
    username = serializers.CharField(
        validators=[validate_username],
        max_length=150,
        required=True,)
    email = serializers.EmailField(
        max_length=254,
        required=True,)


class GetJwtTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена"""
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        sum_score = 0
        if len(reviews) != 0:
            for review in reviews:
                sum_score += review.score
            return sum_score // len(reviews)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор модели Reviews.'''
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('author', 'title')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Один пользователь может оставить только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор модели Comment.'''
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('author', 'review')
