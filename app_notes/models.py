from django.db import models

from django.contrib.auth.models import User
from app_contacts.models import Contact


class Note(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
