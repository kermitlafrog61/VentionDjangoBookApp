from django.contrib import admin
from .models import Book, Author, Genre



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre')

admin.site.register(Author)
admin.site.register(Genre)