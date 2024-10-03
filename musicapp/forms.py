from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.html import mark_safe


# For user registration
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'placeholder': 'Password *'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'placeholder': 'Retype Password *'}))

    class Meta:
        model = User
        fields = ('username', 
                  'email', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Username'})
        self.fields['email'].label = "Email"
        self.fields['password'].label = "Password"
        self.fields['confirm_password'].label = "Confirm Password"

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not confirm_password:
            raise forms.ValidationError("You must confirm your password")
        if password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")

        return confirm_password

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if not data:
            raise forms.ValidationError("Email cannot be Empty")
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(mark_safe(
                "<span style='color: red;'>User with this email already exists</span>"))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data


class LoginForm(forms.Form):
    username =forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password =forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


        #for singer
class SingerForm(forms.ModelForm):
    class Meta:
        model =Singer
        fields = ['name','address','image','dob','nom_of_album']
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'your_name'
            }),
                'address':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'address'
            }),
                'image':forms.ClearableFileInput(attrs={
                'class':'form-control',
            }),
                'dob':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'dob'
            }),
                'nom_of_album':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'nom_of_album'
            }),
        }

        #for songs
class SongsForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = ['name','singer','released_date','musician']
        widgets ={
                'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Song_title'
            }), 
               'singer':forms.Select(attrs={
                'class':'form-control',
            }), 
                'released_date':forms.DateInput(attrs={
                'class':'form-control',
                'placeholder':'released_date'
            }),
                'musician':forms.Select(attrs={
                'class':'form-control',
            }),
    
        }

        #for musician
class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ['name','address','dob']
        widgets ={
                'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'your_name'
            }), 
                'address':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'address'
            }),
                'dob':forms.DateInput(attrs={
                'class':'form-control',
                'placeholder':'dob'
            }),
        }