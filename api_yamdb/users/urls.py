from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import sign_up_user, get_jwt_token, UserViewSet


app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', sign_up_user),
    path('auth/token/', get_jwt_token),
    path('', include(router.urls)),
]