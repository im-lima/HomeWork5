from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Avg, Count

from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

class DirectorListView(APIView):
    def get(self, request):
        directors = Director.objects.annotate(movies_count=Count('movie'))
        data = [
            {
                'id': director.id,
                'name': director.name,
                'movies_count': director.movies_count,
            }
            for director in directors
        ]
        return Response(data)

    def post(self, request):
        serializer = DirectorSerializer(data=request.data)
        if serializer.is_valid():
            director = serializer.save()
            return Response(DirectorSerializer(director).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectorDetailView(APIView):
    def get(self, request, id):
        director = get_object_or_404(Director, id=id)
        serializer = DirectorSerializer(director)
        return Response(serializer.data)

    def put(self, request, id):
        director = get_object_or_404(Director, id=id)
        serializer = DirectorSerializer(director, data=request.data, partial=True)
        if serializer.is_valid():
            director = serializer.save()
            return Response(DirectorSerializer(director).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        director = get_object_or_404(Director, id=id)
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewDetailView(APIView):
    def get(self, request, id):
        review = get_object_or_404(Review, id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

class MovieReviewsView(APIView):
    def get(self, request):
        movies = Movie.objects.annotate(avg_rating=Avg('reviews__stars'))
        data = [
            {
                'id': movie.id,
                'title': movie.title,
                'reviews': [
                    {
                        'id': review.id,
                        'text': review.text,
                        'stars': review.stars,
                    } for review in movie.reviews.all()
                ],
                'average_rating': movie.avg_rating,
            }
            for movie in movies
        ]
        return Response(data)

class DirectorWithMoviesCountView(APIView):
    def get(self, request):
        directors = Director.objects.annotate(movies_count=Count('movie'))
        data = [
            {
                'id': director.id,
                'name': director.name,
                'movies_count': director.movies_count,
            }
            for director in directors
        ]
        return Response(data)