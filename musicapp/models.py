from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
# from django.conf import TimeStampMixin


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

    class Meta:
        abstract = True


class Singer(TimeStampMixin):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='singer/', null=True, blank=True)
    dob = models.DateField(max_length=10)
    nom_of_album = models.IntegerField()
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class Musician(TimeStampMixin):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80, blank=True, null=True)
    dob = models.DateField(max_length=10)

    def __str__(self):
        return self.name
   

class Songs(TimeStampMixin):
    name = models.CharField(max_length=50)
    singer = models.ForeignKey(Singer,on_delete=models.SET_NULL, blank=True, null=True)
    released_date = models.DateField(max_length=10)
    musician = models.ForeignKey(Musician,on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.name
    

 



