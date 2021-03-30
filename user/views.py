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
from django.core.paginator import Paginator

class Home(ListView):
    model=Course
    context_object_name = 'course'
    paginate_by=4
    template_name = 'user/home.html'
    order = ['-rating']
    def get_queryset(self):
        return Course.objects.all().order_by('-created').order_by('-rating')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subject']=Subject.objects.all()
        if self.request.user.is_authenticated:
            try:
                followings=[fol for fol in self.request.user.cprofile.following.all()]
            except:
                try:
                    followings=[fol for fol in self.request.user.vprofile.following.all()]
                except:followings=[]
            folcourse=[]
            for user in followings:
                fol=user.courses_created.all()
                for course in fol:
                    folcourse.append(course)
            folcourse.sort(key=lambda r:r.created,reverse=True)
            paginator1 = Paginator(folcourse, 4)
            page_number1 = self.request.GET.get('page1')
            page_obj1 = paginator1.get_page(page_number1)
            context['page_objfol']=page_obj1
            #context['folcourse']=folcourse

        return context

class CreatorProfile(UserPassesTestMixin,LoginRequiredMixin,CreateView):
    model = CreatorProfile
    fields = ['dob', 'city', 'state', 'image','edu']
    template_name = 'user/creatorprofile.html'
    def test_func(self):
        #if self.request.user.cprofile or self.request.user.vprofile:
        if hasattr(self.request.user, 'cprofile') or hasattr(self.request.user, 'vprofile'):
            return False
        return True
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self,**kwargs):
        return reverse('home')
        #return reverse('question', args=[str(self.kwargs['pk'])])

class ViewerProfile(UserPassesTestMixin,LoginRequiredMixin,CreateView):
    model = ViewerProfile
    fields = ['dob', 'city', 'state', 'image']
    template_name = 'user/viewerprofile.html'
    def test_func(self):
        #if self.request.user.cprofile.exists() or self.request.user.vprofile.exists():
        if hasattr(self.request.user, 'cprofile') or hasattr(self.request.user, 'vprofile'):
            return False
        return True
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self,**kwargs):
        return reverse('home')
