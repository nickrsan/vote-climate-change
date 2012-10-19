# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
#from django.core import serializers

from django.forms import ValidationError

from EC.index import FormMessage, page_item
from EC.db.models import Action
from EC.feedback.models import FeedbackForm,Feedback_Item

def send_feedback(request):
	
	if request.method == "POST":
		data_form = FeedbackForm(request.POST)
		l_message = FormMessage() # prepare to send a message to the user
		
		try:
			if data_form.is_valid():
				submitted_feedback = Feedback_Item(**data_form.cleaned_data) # ** expands a dict into kw args
				submitted_feedback.request_url = request.path
				submitted_feedback.user_agent = request.META['HTTP_USER_AGENT']
				submitted_feedback.created_by_id = 0
				submitted_feedback.save()
				
				if request.is_ajax() == True:
					l_message.status = "success"
			else:
				if request.is_ajax() == True:
					l_message.status = "failed"
					for error_message in data_form.errors:
						l_message.messages.append(error_message)
				else:
					return HttpResponse("failed") # need to render a template here!
		except ValidationError as e:
			if request.is_ajax() == True:
				l_message.status = "failed"
				l_message.messages.append("We encountered a problem validating your submission: %s" % e)
		except:
			raise
			l_message.status = "failed"
			l_message.messages.append("Error processing your request")
			
		if request.is_ajax() == True: # if we've gotten this far, then the form is valid and successfully saved
			return HttpResponse(l_message.to_json()) # serializer must be passed a sequence
		else:
			return HttpResponse("Need non-ajax success page") # need to render a template here!
	else:
		template = loader.get_template("sitewide_form.django")
		l_item = page_item("Send Feedback")
		cont = RequestContext(request,{"page_info":l_item,"formname":"FeedbackForm","formdata":""})
		return HttpResponse(template.render(cont))