from django.urls import include, path
from rest_framework.routers import DefaultRouter 

from .views import (CommentViewSet, ReviewViewSet, TitleViewSet, CategoryViewSet,
                    GenreViewSet,)

from users.views import sign_up_user, get_jwt_token, UserViewSet

router_v1 = DefaultRouter() 
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', 
                   ReviewViewSet, 
                   basename='review')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', 
                   CommentViewSet, 
                   basename='review')
router_v1.register(r'titles/', TitleViewSet, basename='titles')
router_v1.register(r'categories/', CategoryViewSet, basename='categories')
router_v1.register(r'genres/', GenreViewSet, basename='genres')
# router_v1.register(r'users/', UserViewSet, basename='users') #


urlpatterns = [ 
    path('v1/', include(router_v1.urls), name='api-root'),
    # path('v1/auth/signup/', sign_up_user), #
    # path('auth/token/', get_jwt_token), #
    ]

# Рабочий вариант

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter 

# from .views import (CommentViewSet, ReviewViewSet, TitleViewSet, CategoryViewSet,
#                     GenreViewSet,)

# router_v1 = DefaultRouter() 
# router_v1.register(r'titles/(?P<title_id>\d+)/reviews', 
#                    ReviewViewSet, 
#                    basename='review')
# router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', 
#                    CommentViewSet, 
#                    basename='review')
# router_v1.register(r'titles/', TitleViewSet, basename='titles')
# router_v1.register(r'categories/', CategoryViewSet, basename='categories')
# router_v1.register(r'genres/', GenreViewSet, basename='genres')


# urlpatterns = [ 
#     path('v1/', include(router_v1.urls), name='api-root'), 
#     ]
