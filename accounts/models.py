from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class CustomUser(AbstractUser):
    color_skin = models.CharField(max_length=15, null=True,default="brown")
    photo = models.ImageField(upload_to="photos",null=True)
    bio = models.TextField(null=True)

    

