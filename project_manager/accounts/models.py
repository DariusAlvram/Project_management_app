from django.db import models
from django.contrib.auth.models import User
# import django signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timesince import timesince


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    @property
    def profile_picture_url(self):
        try:
            image = self.profile_picture.url
        except ValueError:
            image = 'https://cdn.pixabay.com/photo/2023/05/02/10/35/avatar-7964945_960_720.png'
        return image
    
    # @property
    # def full_name(self):
    #     first_name = self.user.first_name
    #     last_name = self.user.last_name
    #     if first_name and last_name:
    #         return f"{first_name} {last_name}"
    
    @property
    def full_name(self):
        name = self.user.get_full_name()
        if name:
            return name
        else:
            return self.user.username
    
    @property
    def date_joined(self):
        return timesince(self.user.date_joined) + ' ago'
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # if the user is created, and has no profile, create a profile for the user
    Profile.objects.get_or_create(user=instance)

