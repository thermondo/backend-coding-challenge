from django.db import models

from core.models import BaseModel

from django.contrib.auth.models import User


class Tag(BaseModel):
    name = models.CharField(max_length=60, null=False, blank=False)


class Note(BaseModel):
    title = models.CharField(max_length=200, null=False, blank=False)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    is_public = models.BooleanField(default=False)
