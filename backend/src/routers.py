from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from src.reviews import views as reviews
from src.users import views as users

v1_router = routers.DefaultRouter()

v1_router.register('users', users.UsersViewSet, basename='users')
v1_router.register('titles', reviews.TitleViewSet, basename='titles')
v1_router.register('genres', reviews.GenreViewSet, basename='genres')
v1_router.register('categories', reviews.CategoryViewSet, basename='category')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   reviews.ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    reviews.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', users.signup, name='signup'),
    path('v1/auth/token/', users.create_token, name='token'),
    path('redoc/',
         TemplateView.as_view(template_name='redoc.html'), name='redoc')
]
