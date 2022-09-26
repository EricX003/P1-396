from django.forms import ModelForm
from .models import *
from django import forms

class CreateInForum(ModelForm):
    class Meta:
        file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        model = forum
        fields = "__all__"

class CreateInMedia(ModelForm):
    class Meta:
        model = Media
        fields = ['description', 'file']

class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = "__all__"