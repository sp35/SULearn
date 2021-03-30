from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.contrib import admin
from django.db import models
from django.urls import reverse
User._meta.get_field('email')._unique = True

class ViewerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vprofile', verbose_name='username')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics',verbose_name='Profile picture')
    city = models.CharField(verbose_name='City', max_length=100)
    state = models.CharField(verbose_name='State', max_length=100)
    doj = models.DateTimeField(default=timezone.now, verbose_name='Date of Joining')
    dob = models.DateTimeField(default=timezone.now, verbose_name='Date of Birth')
    following = models.ManyToManyField(User,blank=True)
    def __str__(self):
        return f'{self.user.username} ViewerProfile'
    def save(self, *args, **kwargs):
        super(ViewerProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cprofile', verbose_name='username')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics',verbose_name='Profile picture')
    city = models.CharField(verbose_name='City',max_length=100)
    state = models.CharField(verbose_name='State',max_length=100)
    doj=models.DateTimeField(default=timezone.now,verbose_name='Date of Joining')
    dob = models.DateTimeField(default=timezone.now,verbose_name='Date of Birth')
    edu = models.TextField(verbose_name='Education Qualification')
    rating=models.DecimalField(default=0,decimal_places=2,max_digits=3)
    following=models.ManyToManyField(User,blank=True)
    def __str__(self):
        return f'{self.user.username} CreatorProfile'
    def save(self, *args, **kwargs):
        super(CreatorProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



