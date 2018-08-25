from django.db import models
from django.utils import timezone


class Track(models.Model):
    track_name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    uri = models.CharField(max_length=50)
    preview_url = models.CharField(max_length=500, null=True)
    created_date = models.DateTimeField(default=timezone.now) 
    track_id = models.CharField(max_length=50)

    def __str__(self):
        return self.track_name

