from django.db import models

# Create your models here.

class state(models.model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=3)

class style(models.model):
    prefix = models.TextField()
    suffix = models.TextField()
    available = models.BooleanField(default=True)

class statement(models.model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(state,required=False)
    text = models.TextField(required=False)
    style = models.ForeignKey(style)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    highlight = models.BooleanField(default=False)

class image_statement(statement):
    image = models.ImageField()

class audio_statement(statement):
    audio = models.FileField()

class video_statement(statement):
    """
        Using a URL field for the video, because I don't think we'll be able to record video. Better to just point
        people to the correct sites.
    """
    video = models.URLField()

class candidate(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(state)
