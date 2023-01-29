from django.urls import include, path
from rest_framework import routers

from src.reviews.views import CommentViewSet, ReviewViewSet
from src.titles.views import CategoryViewSet, GenreViewSet, TitleViewSet
from src.users.views import UsersViewSet, create_token, signup

v1_router = routers.DefaultRouter()

v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', create_token, name='token')
]
