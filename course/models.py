from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

RATING_CHOICES= (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

class Subject(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['title']
    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,related_name='courses_created',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)
    rating=models.DecimalField(default=0,decimal_places=2,max_digits=4)
    class Meta:
        ordering = ['-subject']

    def __str__(self):
        return self.title

    def get_absolute_url(self, **kwargs):
        return reverse('course-detail', kwargs={'pk':self.pk})

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date=models.DateTimeField(default=timezone.now)
    def get_absolute_url(self,**kwargs):
        return reverse('course-detail', kwargs={'pk': self.course.pk})

    def __str__(self):
        return '{}'.format( self.title)

class Completed(models.Model):
    course = models.ForeignKey(Course,related_name='c_comp',on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='m_comp', on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user_comp',on_delete=models.CASCADE)
    def get_absolute_url(self,**kwargs):
        return reverse('course-detail', kwargs={'pk': self.course.pk})

    def __str__(self):
        return '{}'.format(self.course.title)
class CourseRating(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(choices= RATING_CHOICES,default=1)
    review=models.TextField()

    def __str__(self):
        return self.course.title or ' '


