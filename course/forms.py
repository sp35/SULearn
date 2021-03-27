from django import forms
from django.contrib.auth.models import User
from user.models import CreatorProfile,ViewerProfile


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='last Name', required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class CreatorProfileUpdateForm(forms.ModelForm):
    edu = forms.CharField(label='Education qualification', required=False)

    class Meta:
        model = CreatorProfile
        fields = ['city','state','dob','edu', 'image']

class ViewerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ViewerProfile
        fields = ['city','state','dob', 'image']
