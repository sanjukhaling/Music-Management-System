from musicapp.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


        #for user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id',"username","email"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =["username","email","password"]

        def create(self,validated_data):
            user =User.objects.create_user(
                validated_data["username"],
                validated_data["email"],
                validated_data["password"],
            )
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
            #for singer
class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = ["id","name","address","nom_of_album","image","dob"]




        #SONGS
class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ["id","name","singer","released_date","musician"]


    #MUSICIAN
class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musician
        fields = ["id","name","address","dob"]