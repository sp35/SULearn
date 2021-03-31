from .models import CreatorProfile,ViewerProfile
from django import forms
from django.contrib.auth.models import User

class CreatorForm(forms.ModelForm):
    edu = forms.CharField(required=True,label='Education Qualification')

    class Meta:
        model = CreatorProfile
        exclude = ['user', 'doj','rating']

class ViewerForm(forms.ModelForm):

    class Meta:
        model = ViewerProfile
        exclude = ['user', 'doj']
    '''def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        profile, created = UserProfile.objects.get_or_create(
            user=user, defaults={
                'locality': self.cleaned_data['locality'],
                'voivodship': self.cleaned_data['voivodship'],
                'postcode': self.cleaned_data['postcode'],
                'street': self.cleaned_data['street'],
                'building': self.cleaned_data['building'],
                'premises': self.cleaned_data['premises'],
            })
        if created: # This prevents saving if profile already exist
            profile.save()'''