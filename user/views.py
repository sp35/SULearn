from django.shortcuts import render
from .models import ViewerProfile,CreatorProfile
from django.views.generic import ListView ,DetailView,CreateView,UpdateView,DeleteView
from course.models import Course,Subject,Module
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CreatorForm,ViewerForm
from django.urls import reverse,resolve
from django.http import HttpResponseRedirect,HttpResponseRedirect
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db.models import Count

class Home(ListView):
    model=Course
    context_object_name = 'course'
    template_name = 'user/home.html'
    order = ['-subject']
    def get_queryset(self):
        return Course.objects.all()
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subject']=Subject.objects.all()
        return context



class CreatorProfile(LoginRequiredMixin,CreateView):
    model = CreatorProfile
    fields = ['dob', 'city', 'state', 'image','edu']
    template_name = 'user/creatorprofile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self,**kwargs):
        return reverse('home')
        #return reverse('question', args=[str(self.kwargs['pk'])])

class ViewerProfile(LoginRequiredMixin,CreateView):
    model = ViewerProfile
    fields = ['dob', 'city', 'state', 'image']
    template_name = 'user/viewerprofile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self,**kwargs):
        return reverse(home)
