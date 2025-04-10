from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class NotificationManager(models.Manager):
    def for_user(self, user):
        return self.filter(receipient=user)

    def unread(self, user):
        return self.for_user(user).filter(read=False)
    
    def read(self, user):
        return self.for_user(user).filter(read=True)

class Notification(models.Model):
    receipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_on = models.DateTimeField()
    read = models.BooleanField(default=False)
    
    objects = NotificationManager()
    
    def __str__(self):
        return f'{self.actor} {self.verb} {self.content_object}'
    
    class Meta:
        ordering = ['-created_on']
        
    @property
    def notification_time_formatted(self):
        return self.created_on.strftime('%b %d, %I:%M %p')