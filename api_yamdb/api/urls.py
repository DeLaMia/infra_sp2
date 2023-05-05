from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, signup, login
from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet)

app_name = 'api'


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
v1_router.register(r'titles/(?P<title_id>\d+)/'
                   r'reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', login, name='login'),
]
