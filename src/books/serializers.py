from rest_framework import serializers
from django.db.models import Avg
from django.db import models

from .models import Book, Review, Favorite, Genre, Author


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'book']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['book'] = self.context['book']
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.username
        return ret


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        item_list = data.all() if isinstance(data, models.Manager) else data
        user = self.context['request'].user
        return [{
            'id': item.id,
            'title': item.title,
            'author': item.author.full_name,
            'genre': item.genre.name,
            'average_raiting': item.reviews.aggregate(Avg('rating'))['rating__avg'],
            'is_favorite': Favorite.objects.filter(user=user, book=item).exists(),
        } for item in item_list]


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    author = AuthorSerializer()
    is_favorite = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    average_raiting = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'description', 'genre', 'author', 'average_raiting',
                  'publication_date', 'reviews', 'is_favorite']
        list_serializer_class = BookListSerializer

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return Favorite.objects.filter(user=user, book=obj).exists()

    def get_average_raiting(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']


class FavoriteSerializer(serializers.Serializer):
    """
    Empty serializer for adding/removing favorite books
    """
    pass