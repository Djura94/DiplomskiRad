from django.utils import timezone
from django.db import models
from .imagekit_helper import upload_to_imagekit

# Create your models here.

class Course(models.Model):
    image = models.ImageField(upload_to="images/")
    summary=models.CharField(max_length=200)
    description=models.CharField(max_length=400, default='')
    profesor_link=models.CharField(max_length=100, default='')

    def save(self, *args, **kwargs):
        if self.image:
            self.image = upload_to_imagekit(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.summary

class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,max_length=100)
    created_date=models.DateTimeField('Datum kreiranja', default=timezone.now)

    def __str__(self):
        return self.email