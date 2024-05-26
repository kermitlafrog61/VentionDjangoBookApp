import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    publication_date = django_filters.DateFromToRangeFilter(field_name='publication_date', label='Ignore in swagger')

    class Meta:
        model = Book
        fields = ['genre', 'author']
