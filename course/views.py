from django.shortcuts import render
from .models import Course,Module,Subject,Completed,CourseRating
from user.models import ViewerProfile,CreatorProfile
from django.views.generic import ListView ,DetailView,CreateView,UpdateView,DeleteView
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse,resolve
from django.http import HttpResponseRedirect,HttpResponseRedirect
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db.models import Count
from django.core.paginator import Paginator
from .forms import CreatorProfileUpdateForm,ViewerProfileUpdateForm,UserUpdateForm


class CourseCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Course
    template_name='course/createcourse.html'
    fields=['subject','title','overview']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    def test_func(self):
        creator=[creator for creator in CreatorProfile.objects.all()]
        for c in creator:
            if c.user==self.request.user:
                return True
            else:
                continue
        else:
            False
class AddModule(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Module
    template_name='course/addmodule.html'
    fields=["title",'description','file']
    def form_valid(self, form):
        print(self.kwargs)
        form.instance.course = Course.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    def test_func(self):
        course=Course.objects.get(id=self.kwargs['pk'])
        if self.request.user==course.owner:
            return True
        return False
class CourseDetail(DetailView):
    model=Course
    def get_context_data(self,**kwargs):
        module=Module.objects.filter(course_id=self.kwargs['pk'])
        if Course.objects.get(id=self.kwargs['pk']) in self.request.user.courses_joined.all():
            joined=True
        else:
            joined=False
        if len(self.request.user.user_comp.filter(course_id=self.kwargs['pk']).all())==len(Course.objects.get(id=self.kwargs['pk']).modules.all()):
            coursecomp=True
        else:
            coursecomp=False
        context = super().get_context_data(**kwargs)
        context['joined']=joined
        context['module']=module
        context['review']=CourseRating.objects.filter(course_id=self.kwargs['pk']).all()
        mcom=Completed.objects.filter(user=self.request.user).filter(course_id=self.kwargs['pk']).all()
        modcomp=[mcom.module for mcom in mcom]
        modincomp=[]
        for j in module:
            if j in modcomp:
                continue
            else:
                modincomp.append(j)
        context['modincomp'] = modincomp
        context['modcomp']=modcomp
        context['coursecomp']=coursecomp

        #pagination

        paginator = Paginator(CourseRating.objects.filter(course_id=self.kwargs['pk']).all(), 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CourseDetailNU(DetailView):
    model=Course
    template_name='course/cdnu.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = Module.objects.filter(course_id=self.kwargs['pk'])
        context['module'] = module
        context['review'] = CourseRating.objects.filter(course_id=self.kwargs['pk']).all()
        context['subject']=Subject.objects.all()
        # pagination

        paginator = Paginator(CourseRating.objects.filter(course_id=self.kwargs['pk']).all(), 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


@login_required
def enroll(request,pk):
    course=Course.objects.get(id=pk)
    students=[student for student in course.students.all()]
    if request.user not in students:
        course.students.add(request.user)
    return redirect('course-detail', pk=pk)


@login_required
def complete(request,pk):
    course = Course.objects.get(modules=Module.objects.get(pk=pk))
    students = [student for student in course.students.all()]
    for students in students:
        print(course, students, 'req',request.user)
        if request.user == students:
            comp=Completed.objects.all()
            print(comp)
            if not comp.first():
                Completed.objects.create(user=request.user, course=course, module=Module.objects.get(pk=pk))
                return redirect('course-detail', pk=course.pk)
            else:

                for comp in comp:
                    if comp.user==request.user and comp.module==Module.objects.get(pk=pk):
                        messages.warning(request, 'You have already completed Module')
                        return redirect('course-detail' ,pk=course.pk)
                    else:
                        continue
                else:
                    Completed.objects.create(user=request.user, course=course, module=Module.objects.get(pk=pk))
                    return redirect('course-detail', pk=course.pk)
        else:
            continue
    else:
        messages.warning(request, 'You Have not register in this course')
        return redirect('course-detail', pk=course.pk)

class CourseRate(UserPassesTestMixin,LoginRequiredMixin,CreateView):
    model=CourseRating
    fields=['rate','review']
    template_name='course/courserate.html'
    def form_valid(self, form ,*args,**kwargs):
        rating= CourseRating.objects.filter(course_id=self.kwargs['pk'])
        course=Course.objects.get(id=self.kwargs['pk'])
        creator=CreatorProfile.objects.get(user=course.owner)
        cor=Course.objects.filter(owner=creator.user)
        nc=0
        cor_rate=0
        for course2 in cor:
            cor_rate+=course2.rating

        rating_user=[]
        for rate in rating:
            rating_user.append(rate.user.username)
        if self.request.user.username not in rating_user:
            form.instance.course_id=self.kwargs['pk']
            form.instance.user=self.request.user
            rating1=Course.objects.get(id=self.kwargs['pk'])
            r_s=form.instance.rate
            nu=len(rating_user)+1
            print(type(nu))
            for ques in rating:
                r_s+=ques.rate
            if nu==0:
                ratingf=0
            else:
                ratingf=r_s/nu

            for course1 in cor:

                if course1 == course:
                    if course1.rating==0:
                        cor_rate+=form.instance.rate
                        nc+=1
                    else:
                        print(ratingf)
                        print(cor_rate)
                        print(course1.rating)
                        cor_rate = float(cor_rate)-float(course1.rating)+ratingf
                        print(cor_rate)
                        nc += 1
                else:
                    if course1.rating != 0:
                        nc += 1

            print(type(ratingf))
            print('creator rate', creator.rating)
            #cre_rate = float(creator.rating) + ratingf
            #print(cre_rate)
            if nc==0:
                cre_rating=0
            else:
                cre_rating = cor_rate / nc
            print(cre_rating)

            Course.objects.filter(id=self.kwargs['pk']).update(rating=ratingf)
            CreatorProfile.objects.filter(user=creator.user).update(rating=cre_rating)
            return super().form_valid(form)
        else:
            messages.warning(self.request, 'You have already rated and can not rate once again')
            return HttpResponseRedirect(reverse('course-detail', args=[str(self.kwargs['pk'])]))
    def get_success_url(self,**kwargs):
        return reverse('course-detail', args=[str(self.kwargs['pk'])])
    def test_func(self):
        course=Course.objects.get(id=self.kwargs['pk'])
        if self.request.user in course.students.all() and len(self.request.user.user_comp.filter(course_id=self.kwargs['pk']).all())==len(Course.objects.get(id=self.kwargs['pk']).modules.all()):
            return True
        return False

class ProfileViewerDetail(DetailView):
    model=ViewerProfile
    template_name='course/viewerprofile.html'

    def get_object(self):
        return get_object_or_404(ViewerProfile, user__username=self.kwargs.get('username'))
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        courseenrolled = Course.objects.filter(students__username=self.kwargs['username']).order_by('-created').all()
        coursescompleted = []
        ongoing = []
        for course in Course.objects.filter(students__username=self.kwargs['username']).all():
            if len(self.request.user.user_comp.filter(course_id=course.pk).all()) == len(
                    Course.objects.get(id=course.pk).modules.all()):
                coursescompleted.append(course)
            else:
                ongoing.append(course)
                continue
        context['coursepublished'] = Course.objects.filter(owner__username=self.kwargs['username']).all()
        context['coursecompleted'] = coursescompleted
        context['ongoing'] = ongoing
        # pagination

        paginator1 = Paginator(coursescompleted, 2)
        page_number1 = self.request.GET.get('page1')
        page_obj1 = paginator1.get_page(page_number1)
        context['page_obj1'] = page_obj1

        # pagination

        paginator2 = Paginator(ongoing,2)
        page_number2 = self.request.GET.get('page2')
        page_obj2 = paginator2.get_page(page_number2)
        context['page_obj2'] = page_obj2

        return context

class ProfileCreatorDetail(DetailView):
    model=CreatorProfile
    template_name='course/creatorprofile.html'
    def get_object(self):
        return get_object_or_404(CreatorProfile, user__username=self.kwargs.get('username'))

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        courseenrolled=Course.objects.filter(students__username=self.kwargs['username']).all()
        coursescompleted=[]
        ongoing=[]
        for course in Course.objects.filter(students__username=self.kwargs['username']).all():
            if len(self.request.user.user_comp.filter(course_id=course.pk).all())==len(Course.objects.get(id=course.pk).modules.all()):
                coursescompleted.append(course)
            else:
                ongoing.append(course)
                continue
        context['coursepublished']=Course.objects.filter(owner__username=self.kwargs['username']).order_by('-created').all()
        context['coursecompleted']=coursescompleted
        context['ongoing']=ongoing
        # pagination

        paginator1= Paginator(Course.objects.filter(owner__username=self.kwargs['username']).order_by('-created').all(), 2)
        page_number1 = self.request.GET.get('page1')
        page_obj1 = paginator1.get_page(page_number1)
        context['page_obj1'] = page_obj1

        # pagination

        paginator2 = Paginator(ongoing, 1)
        page_number2 = self.request.GET.get('page2')
        page_obj2 = paginator2.get_page(page_number2)
        context['page_obj2'] = page_obj2

        # pagination

        paginator3 = Paginator(coursescompleted, 1)
        page_number3 = self.request.GET.get('page3')
        page_obj3 = paginator3.get_page(page_number3)
        context['page_obj3'] = page_obj3
        print(page_obj3,coursescompleted)


        return context

@login_required
def creatorprofile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = CreatorProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.cprofile)
        # print('POST',request.POST,'FILE',request.FILES,'USER',request.user,request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = CreatorProfileUpdateForm(instance=request.user.cprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'course/creatorprofile-update.html', context)
@login_required
def viewerprofile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ViewerProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.vprofile)
        # print('POST',request.POST,'FILE',request.FILES,'USER',request.user,request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ViewerProfileUpdateForm(instance=request.user.vprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'course/viewerprofile-update.html', context)

def search(request):
    if request.method == 'GET':
        search =  request.GET.get('search')
        status=[]
        course=[]
        creator=[]
        cr=CreatorProfile.objects.all()
        cs=Course.objects.all()
        for cru in cr:
            if search.lower() in cru.user.username.lower():
                creator.append(cru)
        for cou in cs:
            if search.lower() in cou.title.lower():
                course.append(cou)

        for cou in cs :
            if search.lower() in cou.subject.title.lower():
                status.append(cou)
        return render(request,"course/search.html",{'course':course,'tags':status,'creator':creator})
    else:
        return render(request,"course/search.html",{})

@login_required
def creator_following(request,*args,**kwargs):
    if request.method=='POST':
        try:
            my_profile=ViewerProfile.objects.get(user=request.user)
        except:
            my_profile = CreatorProfile.objects.get(user=request.user)
        print(request.POST)
        creator=CreatorProfile.objects.get(user_id=request.POST.get('profile_pk') )
        if creator.user in my_profile.following.all():
            my_profile.following.remove(creator.user)
        else:
            my_profile.following.add(creator.user)
        return redirect(request.META.get('HTTP_REFERER')   )
    return redirect('profile-detail' , kwargs={ 'pk': request.POST.get('profile_pk')})

class CreatorProfilenu(DetailView):
    model=CreatorProfile
    template_name='course/creatorprofilenu.html'
    def get_object(self,**kwargs):
        return get_object_or_404(CreatorProfile, user_id=self.kwargs.get('pk'))
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course=Course.objects.filter(owner_id=self.kwargs['pk']).all()
        context['coursepublished']=course
        return context

class SubjectList(ListView):
    template_name='course/subject.html'
    context_object_name='subject'
    def get_queryset(self):
        return Subject.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.filter(subject_id=self.kwargs['pk']).order_by('-rating').all()
        context['subject'] = Subject.objects.all()
        context['sub']=Subject.objects.get(id=self.kwargs['pk'])
        paginator = Paginator(Course.objects.filter(subject_id=self.kwargs['pk']).order_by('-rating').all(), 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context

class ModuleDetail(UserPassesTestMixin,LoginRequiredMixin,DetailView):
    model= Module
    template_name='course/moduledetail.html'
    def test_func(self,**kwargs):
        module=Module.objects.get(id=self.kwargs['pk'])
        if self.request.user in module.course.students.all() or self.request.user == module.course.owner:
            return True
        else:
            return False
