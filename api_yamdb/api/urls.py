from django.urls import include, path
from rest_framework.routers import DefaultRouter 

from .views import (CommentViewSet, ReviewViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet)

router_v1 = DefaultRouter() 
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', 
                   ReviewViewSet, 
                   basename='review')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', 
                   CommentViewSet, 
                   basename='review')
router_v1.register(r'categories/', CategoryViewSet, basename='category')
router_v1.register(r'genres/', GenreViewSet, basename='genre')
router_v1.register(r'titles/', TitleViewSet, basename='title')


urlpatterns = [ 
    path('v1/', include(router_v1.urls), name='api-root'), 
    ] 