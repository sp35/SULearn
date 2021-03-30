from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from user.models import CreatorProfile
from django.core.mail import send_mail
from SULearn.settings import EMAIL_HOST_USER
from .models import Course

@receiver(post_save, sender=Course)
def send_post_mail(sender , instance, created, **kwargs):
    if created:
        print('sent mail')
        recepients = []

        for i in instance.owner.cprofile.following.all():
            recepients.append(str(i.email))
        send_mail('New course update from '+str(instance.owner.username), str(instance.title), EMAIL_HOST_USER, recepients, fail_silently=False)
        pass