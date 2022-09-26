import uuid
from django.db import models 
import datetime
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import os

'''
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
'''

User = get_user_model()

class NewIndicator(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    newPost = models.BooleanField(default=False)

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class forum(models.Model):
    
    views = models.IntegerField(default = 0, editable = False)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, default = "Anonymous")
    topic = models.CharField(max_length=300, default='Untitled')
    description = models.CharField(max_length=1000, default = '')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.topic)

class Discussion(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, default = "Anonymous")
    forum = models.ForeignKey(forum, on_delete=models.CASCADE,  blank = False)
    comment = models.CharField(max_length = 500)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.forum)

class Media(models.Model):

    class Meta:
        verbose_name = 'media'
        verbose_name_plural = 'media'
    
    file = models.FileField(null=False, blank=False)
    description = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.description