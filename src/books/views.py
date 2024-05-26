from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import BookFilter
from .models import Book, Favorite, Review
from .permissions import IsAuthor
from .serializers import BookSerializer, FavoriteSerializer, ReviewSerializer


class BookViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == 'favorite':
            return FavoriteSerializer
        return BookSerializer

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        book = self.get_object()
        favor = Favorite.objects.filter(user=request.user, book=book)
        if favor.exists():
            favor.delete()
            return Response({'message': 'deleted from favorites'}, status=status.HTTP_204_NO_CONTENT)
        else:
            Favorite.objects.create(user=request.user, book=book)
            return Response({'message': 'added to favorites'}, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('genre', openapi.IN_QUERY,
                              description="Filter by genre", type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY,
                              description="Filter by author", type=openapi.TYPE_STRING),
            openapi.Parameter('publication_date_after', openapi.IN_QUERY,
                              description="Filter by publication date after (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('publication_date_before', openapi.IN_QUERY,
                              description="Filter by publication date before (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsAuthor()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        context['book'] = get_object_or_404(Book, id=self.kwargs['id'])
        return context
