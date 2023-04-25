from rest_framework.routers import DefaultRouter 

from .views import ReviewViewSet

router_v1 = DefaultRouter() 
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', 
                   ReviewViewSet, 
                   basename='review') 


 

# urlpatterns = [ 
#     path('v1/', include(router_v1.urls), name='api-root'), 
#     path('v1/', include('djoser.urls.jwt')), 
# ] 