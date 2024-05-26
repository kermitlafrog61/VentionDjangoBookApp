from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, ReviewViewSet

router = DefaultRouter()
router.register('book', BookViewSet, 'books')
router.register(r'book/(?P<id>\d+)/review', ReviewViewSet, 'reviews')

urlpatterns = router.urls
