from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, UserSerializer, ConfirmUserSerializer
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework.permissions import AllowAny
from .models import Director, Movie, Review

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.generate_confirmation_code()
            return Response({'message': 'User registered, please check your email for confirmation code.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = get_user_model().objects.get(confirmation_code=serializer.validated_data['confirmation_code'])
                user.is_active = True
                user.confirmation_code = ''
                user.save()
                return Response({'message': 'User confirmed successfully.'}, status=status.HTTP_200_OK)
            except get_user_model().DoesNotExist:
                return Response({'error': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(username=username)
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                return Response({'error': 'User not confirmed yet.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetailView(APIView):
    def get(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            movie = serializer.save()
            return Response(MovieSerializer(movie).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def get(self, request, id):
        review = get_object_or_404(Review, id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, id):
        review = get_object_or_404(Review, id=id)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            review = serializer.save()
            return Response(ReviewSerializer(review).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        review = get_object_or_404(Review, id=id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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