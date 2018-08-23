from django.db import models
from django.utils import timezone


class Track(models.Model):
    track_name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    uri = models.CharField(max_length=50)
    preview_url = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.track_name

