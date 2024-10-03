from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("api/auth/register", RegisterUser.as_view(), name="auth_register"),
    path("api/auth/login", LoginView.as_view(), name="auth_login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

            #SINGER
    path("singer/list-api/", SingerListAPIView.as_view(), name="singerlist_api"),
    path("singer/detail-api/<int:id>", SingerDetailAPIView.as_view(), name="singerdetail_api"),
    path("singer/create-api/", SingerCreateAPIView.as_view(), name="singer_create"),
    path("singer/update/<int:id>", SingerUpdateAPIView.as_view(), name="singer_update"),
    path("singer/delete/<int:id>", SingerDeleteAPIView.as_view(), name ="singer_delete"),

        #SONGS
    path("songlist-api/", SongsListAPIView.as_view(), name="songs_list"),
    path("songs/detail/<int:id>/", SongsDetailAPIView.as_view(), name="songs_detail"),
    path("songs/create/", SongsCreateAPIView.as_view(), name="songs_create"),
    path("songsdelete/<int:id>/", SongsDeleteAPIView.as_view(), name="songs_delete"),

        #MUSICIAN
    path("musician/list/", MusicianListAPIView.as_view(),name ="musician_list"),
    path("musician/create/", MusicianCreateAPIView.as_view(), name="musician_create"),
    path("musician/update/<int:id>/", MusicianUpdateAPIView.as_view(), name="musician_update"),
    path("musician/delete/<int:id>/", MusicianDeleteAPIView.as_view(), name="musician_delete"),

]   