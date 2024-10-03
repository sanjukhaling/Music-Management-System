from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import HttpResponse

from rest_framework import status

import base64
from PIL import Image
from io import BytesIO
import os
import random
from datetime import datetime
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.contrib.auth import authenticate


        #for register
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


#Login
class LoginView(generics.GenericAPIView):
    seralizer_class = LoginSerializer

    def post(self,request,*args,**kwargs):
        username = request.data.get(username)
        password = request.data.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            })
        else:
            return Response({'invalid credential,'})



        #SINGER
        # for singer 
class SingerListAPIView(APIView):
    permission_classes = (IsAuthenticated)

    def get(self,request):
        singers = Singer.objects.all()
        serializer = SingerSerializer(singers, many=True)
        res ={
            'data':serializer.data
        }
        return Response(res,status=200)


        #for detail

class SingerDetailAPIView(APIView):
    def get(self, request, id):
        try:
            singer = Singer.objects.get(id=id)
            return Response({'status': 'success', 'data': SingerSerializer(singer).data}, status=200)
        except Singer.DoesNotExist:
            return Response({'status': 'error', 'message': 'Singer not found.'}, status=404)

    def post(self, request):
        image = self.base64_to_image(request.data.get('photo'), "/home/sanju/Desktop/sanju/FinalProject/mms/mproject/media/singer")
        request.data['image'] = image
        # Proceed with handling the rest of the POST request

    def base64_to_image(self, base64_string, file_path):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            image = Image.open(BytesIO(base64.b64decode(base64_string)))
            image_name = f"st-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{random.randint(100, 999)}.jpg"
            image.save(os.path.join(file_path, image_name), "JPEG")
            return os.path.join(file_path, image_name)
        except Exception as e:
            print(f"Error: {e}")
            return None


        #for create
class SingerCreateAPIView(APIView):
    def post(self, request):
        try:
            serializer = SingerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            res = {
                'status': 'Sorry! An error occurred during creation.',
                'error': str(e),
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        #for update
class SingerUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            singer = Singer.objects.get(id=id)
            serializer = SingerSerializer(singer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Singer.DoesNotExist:
            res = {
                'status': 'Singer not found.',
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)


        #for delete
class SingerDeleteAPIView(APIView):
    def delete(self,request,id):
        try:
            singer_id = Singer.objects.get(id=id)
            singer_id.delete()
            res = {
                'status': 'success'
            }
            return Response(res,status=200)
        except Singer.DoesNotExist:
            res = {
                'status': 'deleting errors'
            }
            return Response(res,status=400)


        #SONGS
class SongsListAPIView(APIView):

    def get(self,request):
        try:
            songs = Songs.objects.all()
            serializers = SongsSerializer(songs,many=True)
            res = {
                'data': serializers.data,

            }
            return Response(res,status=200)
        except Songs.DoesNotExist:
            res = {
                'status': 'sorry!!'
            }
            return Response(res,status=400)


        #for detail
class SongsDetailAPIView(APIView):
    def get(self, request, id):
        try:
            # Fetch the song by ID
            song = Songs.objects.get(id=id)
            song_serializer = SongsSerializer(song)
            
            # Prepare the response with song data
            res = {
                'data': {
                    'status': 'success',
                    'song': song_serializer.data,
                    'singer': self.get_related_data(song.singer, SingerSerializer, 'Singer'),
                    'musician': self.get_related_data(song.musician, MusicianSerializer, 'Musician')
                }
            }
            return Response(res, status=status.HTTP_200_OK)
        except Songs.DoesNotExist:
            return Response({'status': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)


        #for create
class SongsCreateAPIView(APIView):
    def post(self,request):
        try :
            serializers = SongsSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,status=200)
            else:
                return Response(serializers.errors,status=400)
        except Songs.DoesNotExist:
            res = {
                'status': 'sorry!!'
            }
            return Response(res, status=500)


        #for delete
class SongsDeleteAPIView(APIView):
    def delete(self,request,id):
        try:
            songs = Songs.objects.get(id=id)
            songs.delete()
            resp = {
                'status': 'delete success'
            }
            return Response(resp,status=200)
        except Singer.DoesNotExist:
            res = {
                'status': 'sorry!!'
            }
            return Response(res, status=500)


    #MUSICIAN
    #for list
class MusicianListAPIView(APIView):
    permission_classes = (IsAuthenticated)

    def get(self,request):
        try:
            musician = Musician.objects.all()
            serializers = MusicianSerializer(musician,many=True)
            res ={
                'data':serializers.data,
            }
            return Response(res,status=200)
        except Musician.DoesNotExist:
            res = {
                'status': 'sorry!!!'
            }
            return Response(res,status=500)


    #for create
class MusicianCreateAPIView(APIView):
    def post(self,request):
        try:
            serializers = MusicianSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=200)
            else:
                res = {
                    'data': serializers.errors,
                    'status': 'creating data errors'
                }
                return Response(res, status=400)
        except Musician.DoesNotExist:
            res = {
                'status':'sorry !!'
            }
            return Response(res,status=500)


        #for delete
class MusicianDeleteAPIView(APIView):
    def delete(self,request,id):
        try:
            songs = Songs.objects.get(id=id)
            songs.delete()
            resp = {
                'status': 'delete success'
            }
            return Response(resp,status=200)
        except Singer.DoesNotExist:
            res = {
                'status': 'sorry!!'
            }
            return Response(res, status=500)


    #for update
class MusicianUpdateAPIView(APIView):
    def put(self, request, id):
        try:
            musician = Musician.objects.get(id=id)
            serializer = MusicianSerializer(musician, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Singer.DoesNotExist:
            res = {
                'status': 'musician not found.',
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
