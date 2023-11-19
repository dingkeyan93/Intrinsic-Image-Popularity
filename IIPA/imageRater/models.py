from django.db import models
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid


# Create your models here.
class ImageRating(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    image = models.ImageField()
    rating = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ImageRatingForm(forms.ModelForm):
    class Meta:
        model = ImageRating
        fields = ["image"]
