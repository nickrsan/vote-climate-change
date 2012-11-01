from django.db import models
from django import forms
from django.core import exceptions

# Create your models here.
import global_funcs
import utils
import simplejson as json

class state(models.Model):
	name = models.CharField(max_length=255)
	abbreviation = models.CharField(max_length=4)
	fips_code = models.IntegerField(null=True)

class user(models.Model):
	name = models.CharField(max_length=255)
	ip = models.IPAddressField()
	state = models.ForeignKey(state,null=True)

class style(models.Model):
	name = models.CharField(max_length=255)
	publisher = models.CharField(max_length=50) # the publisher template to use
	template_string = models.TextField()
	available = models.BooleanField(default=True)
	output_template = models.CharField(max_length=255,null=False)
	twitter_template = models.CharField(max_length=200)

class candidate(models.Model):
	name = models.CharField(max_length=255)
	state = models.ForeignKey(state,null=True)
	district = models.CharField(max_length=50,null=True)
	gender = models.CharField(max_length=5,null=True)
	senate_class = models.CharField(max_length=5,null=True)
	webform_url = models.URLField(null=True)
	twitter_handle = models.CharField(max_length=255,null=True)
	party = models.CharField(max_length=5, null=True)
	level = models.CharField(max_length=50, null=True)

	# the following are for matching searches
	bioguide_id = models.CharField(max_length=50,null=True)
	fec_id = models.CharField(max_length=50, null=True)
	crp_id = models.CharField(max_length=50, null=True)
	votesmart_id = models.CharField(max_length=50, null=True)
	govtrack_id = models.CharField(max_length=50, null=True)
	leg_id = models.CharField(max_length=50, null=True)
	transparencydata_id = models.CharField(max_length=50, null=True)
	nimsp_id = models.CharField(max_length=50, null=True)
	photo_url = models.URLField(null=True)
	congresspedia_url = models.URLField(null=True)

	unconfirmed = models.BooleanField(default=False)
	user_submitted = models.BooleanField(default=False)
	submitted_by = models.ForeignKey(user,null=True)

	def __str__(self):
		return self.__unicode__(self)

	def __unicode__(self):
		uni_str = "%s\n%s\n%s\n" % (self.name,self.state.name,self.district)
		return uni_str

	def to_json(self):
		if self.state:
			state_abbrev = self.state.abbreviation,
		else:
			state_abbrev = None
		return json.dumps(
			{
			'cand_id': self.id,
			'name': self.name,
			'state_abbrev': state_abbrev,
			'congresspedia_url': self.congresspedia_url,
			'twitter_handle': self.twitter_handle,
			'gender':self.gender,
			}
		)

class statement(models.Model):
	user = models.ForeignKey(user)
	text = models.TextField(null=True)
	extra_text = models.TextField(null=True)
	rendered_text = models.TextField(null=True)
	style = models.ForeignKey(style)
	date_added = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	highlight = models.BooleanField(default=False)
	hidden = models.BooleanField(default=False)

	support_style = models.CharField(max_length=255,choices=(("I'm voting for","I'm voting for"),("I support","I support")))

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

class sunlight_search (models.Model):
	"""
		meant to track what searches we've done with sunlight so we don't double up
	"""

	search = models.CharField(max_length=255)

class visit(models.Model):
	user = models.ForeignKey(user)
	time_visited = models.DateTimeField(auto_now_add=True)

class random_manager(models.Manager):
	"""
		Intended to return a random object or set of objects
		from a model
	"""
	pass

class ImageUploadForm(forms.Form):
	file  = forms.FileField()

class publisher_form(forms.ModelForm):
	# TODO: make the actual publisher form use these
	# TODO: Add Honeypot

	class Meta:
		model=statement
		fields=('support_style',)

	def __init__(self, *args, **kwargs):
		"""
			Set up this way to allow access to IP address during validation. Thanks to http://stackoverflow.com/questions/1418611/django-forms-clean-method-need-ip-address-of-client
		"""
		self.request_ip = kwargs.pop('request_ip', None)
		super(publisher_form, self).__init__(*args, **kwargs)


	person_name = forms.CharField()
	state = forms.CharField()
	style_id = forms.IntegerField(widget=forms.HiddenInput())
	extra_text = forms.CharField(widget=forms.Textarea(),required=False)
	candidate = forms.CharField()
	candidate_id = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	#support_style = forms.ChoiceField()

	def clean_state(self):
		state_name = self.cleaned_data['state']
		state_name = global_funcs.strip_tags(state_name) # get rid of any HTML

		# replace the cleaned_data['state'] with the object
		self.cleaned_data['state'] = utils.find_state(abbrev=state_name)
		return self.cleaned_data['state']



	def clean(self):
		cleaned_data = super(publisher_form,self).clean()
		if not 'candidate_id' in self.cleaned_data:
			candidate_id = None
		else:
			candidate_id = self.cleaned_data['candidate_id']

		cleaned_data['user_object'] = utils.find_or_make_user(cleaned_data['person_name'],self.request_ip,cleaned_data['state'])

		if candidate_id: # if they provided a candidate_id
			try:
				cleaned_data['candidate'] = candidate.objects.get(pk=candidate_id)
			except candidate.DoesNotExist:
				raise exceptions.ValidationError('Candidate ID was set, but does not correspond to an actual candidate')
		else:
			# ok, now make it do the magic of finding a candidate by name
			if cleaned_data['candidate']:
				try:
					# TODO: This should be a single candidate and in some cases, it's returning more than one
					cleaned_data['candidate'] = utils.find_or_make_candidate(cleaned_data['candidate'],cleaned_data['user_object'])
				except:
					raise
					raise exceptions.ValidationError("Problem looking up candidate. We hope this is temporary. Would you care to try again?")
			else:
				raise exceptions.ValidationError("No candidate provided. Who are you planning on voting for?")

		if utils.isiterable(cleaned_data['candidate']):
			# if it would result in multiple candidates, just take the first
			cleaned_data['candidate'] = cleaned_data['candidate'][0]

		return cleaned_data


