from django.urls import path
from .views import *
 

app_name = 'musicapp'


urlpatterns = [

            #for singer
    path('singer/add', SingerAddView.as_view(), name ='singer_add'),
    path('singer/list', SingerListView.as_view(), name='singer_list'),
    path('singer/<int:id>update', SingerUpdateView.as_view(), name='singer_update'),
    path('singer/<int:id>-delete', SingerDeleteView.as_view(), name='singer_delete'),
    path('singer/<int:id>-detail', SingerDetailView.as_view(), name='singer_detail'),


            #for signup/login/logout
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/page', AdminLoginView.as_view(), name ='admin_login'),
    path('logout/page', AdminLogoutView.as_view(), name ='logout'),


            #for musician
    path('musician/add', MusicianAddView.as_view(), name='musician_add'),
    path('musician/list', MusicianListView.as_view(), name='musician_list'),
    path('musician/<int:id>detail', MusicianDetailView.as_view(), name='musician_detail'),
    path('musician/<int:id>update', MusicianUpdateView.as_view(), name='musician_update'),
    path('musician/<int:id>delete', MusicianDeleteView.as_view(), name='musician_delete'),

            #for songs
    path('songs/<int:id>-add', SongsAddView.as_view(), name='songs_add'),
    path('songs/add2', songsAdd2View.as_view(), name="songs_add2"),
    path('songs/list', SongsListView.as_view(), name='songs_list'),
    path('songs/<int:id>update', SongUpdateView.as_view(), name='songs_update'),
    path('songs/<int:id>delete', SongDeleteView.as_view(), name='songs_delete'),







]
