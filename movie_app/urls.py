from django.urls import path
from .views import (
    DirectorListView,
    DirectorDetailView,
    MovieListView,
    MovieDetailView,
    ReviewListView,
    ReviewDetailView,
    MovieReviewsView,
    RegisterUserView,
    ConfirmUserView,
    LoginUserView,
)

urlpatterns = [
    path('api/v1/directors/', DirectorListView.as_view(), name='directors_list'),
    path('api/v1/directors/<int:id>/', DirectorDetailView.as_view(), name='director_detail'),
    path('api/v1/movies/', MovieListView.as_view(), name='movie_list'),
    path('api/v1/movies/<int:id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('api/v1/movies/reviews/', MovieReviewsView.as_view(), name='movies_with_reviews'),
    path('api/v1/reviews/', ReviewListView.as_view(), name='review_list'),
    path('api/v1/reviews/<int:id>/', ReviewDetailView.as_view(), name='review_detail'),
    path('api/v1/register/', RegisterUserView.as_view(), name='register'),
    path('api/v1/confirm/', ConfirmUserView.as_view(), name='confirm'),
    path('api/v1/login/', LoginUserView.as_view(), name='login'),
]