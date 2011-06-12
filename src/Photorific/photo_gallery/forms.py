from django import forms
from django.contrib.auth import forms as auth_forms

class AddPhotoForm(forms.Form):
    photo = forms.ImageField(label='Photo')
    photo_name = forms.CharField(label='Photo Name')
    comments = forms.CharField(label='Comments', widget=forms.Textarea())

class RegisterUserForm(auth_forms.UserCreationForm):
    fname = forms.CharField(label='First Name')
    lname = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    
class AddAlbumForm(forms.Form):
    name = forms.CharField(label='Album Name')