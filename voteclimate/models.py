from django.db import models

# Create your models here.

class state(models.Model):
	name = models.CharField(max_length=255)
	abbreviation = models.CharField(max_length=3)

class user(models.Model):
	ip = models.IPAddressField()

class style(models.Model):
	name = models.CharField(max_length=255)
	publisher = models.CharField(max_length=50) # the publisher template to use
	template_string = models.TextField()
	available = models.BooleanField(default=True)

class statement(models.Model):
	name = models.CharField(max_length=255)
	state = models.ForeignKey(state,null=True)
	text = models.TextField(null=True)
	extra_text = models.TextField(null=True)
	rendered_text = models.TextField(null=True)
	style = models.ForeignKey(style)
	date_added = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	highlight = models.BooleanField(default=False)
	hidden = models.BooleanField(default=False)

class image_statement(statement):
	image = models.ImageField(upload_to="images/%Y/%m/%d")

class audio_statement(statement):
	audio = models.FileField(upload_to="audio/%Y/%m/%d")

class video_statement(statement):
	"""
		Using a URL field for the video, because I don't think we'll be able to record video. Better to just point
		people to the correct sites.
	"""
	video = models.URLField()

class candidate(models.Model):
	name = models.CharField(max_length=255)
	state = models.ForeignKey(state)

class fact(models.Model):
	statement = models.TextField()
	short_statement = models.CharField(max_length=255,null=True)
	source = models.URLField()
	source_name = models.CharField(max_length=255)
	cite = models.TextField(null=True)

class visit(models.Model):
	user = models.ForeignKey(user)
	time_visited = models.DateTimeField(auto_now_add=True)

class random_manager():
	"""
		Intended to return a random object or set of objects
		from a model
	"""
	pass