from rest_framework import serializers
from .models import Director, Movie, Review
from django.core.exceptions import ValidationError

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be empty.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Title cannot be empty.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be a positive integer.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if not 1 <= value <= 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_text(self, value):
        if not value.strip():
            raise ValidationError("Review text cannot be empty.")
        return value