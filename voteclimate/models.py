from django.db import models
from django import forms
from django.core import exceptions

# Create your models here.
import global_funcs
import utils

class state(models.Model):
	name = models.CharField(max_length=255)
	abbreviation = models.CharField(max_length=4)
	fips_code = models.IntegerField(null=True)

class user(models.Model):
	ip = models.IPAddressField()

class style(models.Model):
	name = models.CharField(max_length=255)
	publisher = models.CharField(max_length=50) # the publisher template to use
	template_string = models.TextField()
	available = models.BooleanField(default=True)
	output_template = models.CharField(max_length=255,null=False)


class candidate(models.Model):
	name = models.CharField(max_length=255)
	state = models.ForeignKey(state)
	district = models.CharField(max_length=5,null=True)
	senate_class = models.CharField(max_length=5,null=True)
	webform_url = models.URLField(null=True)
	party = models.CharField(max_length=5, null=True)

	# the following are for matching searches
	fec_id = models.CharField(max_length=50, null=True)
	crp_id = models.CharField(max_length=50, null=True)
	votesmart_id = models.CharField(max_length=50, null=True)
	govtrack_id = models.CharField(max_length=50, null=True)

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

	candidate = models.ForeignKey(candidate)

	image = models.ImageField(upload_to="images/%Y/%m/%d",null=True)
	audio = models.FileField(upload_to="audio/%Y/%m/%d",null=True)

	# 	Using a URL field for the video, because I don't think we'll be able to record video. Better to just point
	# 	people to the correct sites.

	video = models.URLField(null=True)


class fact(models.Model):
	statement = models.TextField()
	short_statement = models.CharField(max_length=255,null=True)
	source = models.URLField()
	source_name = models.CharField(max_length=255)
	cite = models.TextField(null=True)

class visit(models.Model):
	user = models.ForeignKey(user)
	time_visited = models.DateTimeField(auto_now_add=True)

class random_manager(models.Manager):
	"""
		Intended to return a random object or set of objects
		from a model
	"""
	pass

class publisher_form(forms.Form):
	# TODO: make the actual publisher form use these
	person_name = forms.CharField()
	state = forms.CharField()
	style_id = forms.IntegerField(widget=forms.HiddenInput())
	candidate = forms.CharField()
	candidate_id = forms.IntegerField(widget=forms.HiddenInput())

	def clean_state(self):
		state_name = self.cleaned_data['state']
		state_name = global_funcs.strip_tags(state_name) # get rid of any HTML

		# replace the cleaned_data['state'] wiith the object
		return utils.find_state(abbrev=state_name)

	def clean(self):
		candidate_id = self.cleaned_data['candidate_id']
		if candidate_id: # if they provided a candidate_id
			try:
				self.cleaned_data['candidate'] = candidate.objects.get(pk=candidate_id)
			except candidate.DoesNotExist:
				raise exceptions.ValidationError('Candidate ID was set, but does not correspond to an actual candidate')
		else:
			# ok, now make it do the magic of finding a candidate by name
			candidate_name = self.cleaned_data['candidate']
			if candidate_name:
				self.cleaned_data['candidate'] = utils.find_candidate(self.cleaned_data['candidate'])
			else:
				raise exceptions.ValidationError("No candidate provided. Who are you planning on voting for?")
