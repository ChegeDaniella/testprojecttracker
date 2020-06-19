from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

class Cohort(models.Model):
    name= models.CharField(max_length=255)   

class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.jpg" ,upload_to='images')
    bio = models.CharField(max_length=255,blank=True,null=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    


