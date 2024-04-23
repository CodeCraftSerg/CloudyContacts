from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=20, unique=False,  default="Name", null=False)
    surname = models.CharField(max_length=20, unique=False,  default="Surname", null=False)
    email = models.EmailField(unique=True, null=True)
    mobile_phone = models.CharField(max_length=20, null=True, unique=True)
    work_phone = models.CharField(max_length=20, null=True, unique=True)
    home_phone = models.CharField(max_length=20, null=True, unique=False)
    birthdate = models.DateField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    tiktok = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
