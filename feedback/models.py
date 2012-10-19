from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

from EC import globals

class Feedback_Item(models.Model):
	feedback = models.TextField()
	user_agent = models.TextField()
	email = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	created_by = models.ForeignKey(User)
	page_html = models.TextField()
	dom_item_text = models.TextField()
	dom_item_html = models.TextField()
	browser_url = models.CharField(max_length=255) # the location the browser reports
	request_url = models.CharField(max_length=255)
	
	
class FeedbackForm(models.forms.ModelForm):
	
	action_url = globals.FEEDBACK_URL
	submit_text = "Send Feedback"
	
	# the following are all required = False because we don't want the user to receive a nonsensical error if something
	# goes wrong when setting these fields in JS. We'll notice that something is wrong when submissions come in *without* this info.
	dom_item_text = forms.CharField(widget=forms.HiddenInput(),label="Selected Text", required=False)
	page_html = forms.CharField(widget=forms.HiddenInput(), required=False)
	dom_item_html = forms.CharField(widget=forms.HiddenInput(), required=False)
	browser_url = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Feedback_Item
		exclude = ["created_by", "user_agent","request_url"]