from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, ReviewViewSet,
                    GenreViewSet, TitleViewSet, CategoryViewSet,)
from api.views import sign_up_user, get_jwt_token, UserViewSet

app_name = 'users'
app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls), name='api-root'),
    path('v1/auth/signup/', sign_up_user),
    path('v1/auth/token/', get_jwt_token),
    path('', include(router_v1.urls)),
]
