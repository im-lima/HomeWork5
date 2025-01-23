from django.db import models
import random
import string

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=1,
        verbose_name="Рейтинг"
    )
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review for {self.movie.title} - {self.stars} stars"


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=6, blank=True)

    def generate_confirmation_code(self):
        self.confirmation_code = ''.join(random.choices(string.digits, k=6))
        self.save()

    def __str__(self):
        return self.username