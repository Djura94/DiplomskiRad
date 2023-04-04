from django.db import models

# Create your models here.

class Course(models.Model):
    image = models.ImageField(upload_to="images/")
    summary=models.CharField(max_length=200)
    description=models.CharField(max_length=400, default='')
    profesor_link=models.CharField(max_length=100, default='')


    def __str__(self):
        return self.summary
