from django.urls import include, path
from rest_framework.routers import DefaultRouter 

from .views import CommentViewSet, ReviewViewSet, GenreViewSet, TitleViewSet, CategoryViewSet
from users.views import sign_up_user, get_jwt_token, UserViewSet


router_v1 = DefaultRouter() 
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', 
                   ReviewViewSet, 
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', 
                   CommentViewSet, 
                   basename='comments')
router_v1.register('genres', 
                   GenreViewSet, 
                   basename='genres')
router_v1.register('titles', 
                   TitleViewSet, 
                   basename='titles')
router_v1.register('categories', 
                   CategoryViewSet, 
                   basename='categories')
router_v1.register('users', UserViewSet, basename='users')

# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
# http://127.0.0.1:8000/api/v1/categories/
# http://127.0.0.1:8000/api/v1/genres/

urlpatterns = [ 
    path('v1/', include(router_v1.urls), name='api-root'),
    path('auth/signup', sign_up_user),
    path('auth/token/', get_jwt_token),
    ] 