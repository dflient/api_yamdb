from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet


router = SimpleRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls))
]
