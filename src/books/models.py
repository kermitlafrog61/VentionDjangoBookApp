from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    about = models.TextField()
    # We can add some additional fields, such as working years.
    # But, I'd like to stick with the given task for now

    def __str__(self) -> str:
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, null=True, on_delete=models.SET_NULL, related_name='books')
    description = models.TextField()
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])

    def __str__(self) -> str:
        return f"{self.author.username} --- {self.book.title}"

    class Meta:
        unique_together = ('author', 'book')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
