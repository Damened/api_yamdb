from rest_framework import serializers 

# from rest_framework.validators import UniqueTogetherValidator возможно понадобится для валидации уникальности сочетания полей

from reviews.models import Comment, Review, User

class ReviewSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Reviews.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Review 
        fields = ('__all__') 
        read_only_fields = ('author', 'title')


class CommentSerializer(serializers.ModelSerializer): 
    '''Сериализатор модели Comment.''' 
    author = serializers.SlugRelatedField( 
        slug_field='username', 
        read_only=True) 
 
    class Meta: 
        model = Comment 
        fields = ('__all__') 
        read_only_fields = ('author', 'review')