# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext

from models import statement, fact, style, publisher_form

def log(msg):
	# 	TODO: needs to be fized by the time we go live

	print msg

try:
	import sunlight
except:
	log("Couldn't import sunlight")
	raise


def home(request):

	# set the publisher
	publisher_style = style.objects.get(name="voting_for")

	facts = fact.objects.all()[:8]

	statements = statement.objects.all()[:100]

	template = loader.get_template("index.django")
	cont = RequestContext(request,{'title':"Vote Climate Change",
								   'publisher':publisher_style.publisher,
								   'style_id':publisher_style.id,
								   'facts':facts,
								   'statements':statements,
								   })

	# need RequestContext
	return HttpResponse(template.render(cont))

def add_statement(request):

	data = None
	if request.is_ajax():
		#TODO Make this part work
		pass
	if request.POST:
		data = request.POST
	elif request.GET:
		data = request.GET

	statement_form = publisher_form(data)
	if statement_form.is_valid():
		added_style = style.objects.get(pk=statement_form.cleaned_data['style'])
		name = statement_form.cleaned_data['person_name']

		# next: if candidate doesn't exist - should check the existing candidates first
		# then check the sunlight api. This way it learns as people add them

		# then make a candidate record (function)

		# if it does, use it

		return redirect("/")


def find_electable(request, search_string= None):
	# TODO implement search
	return search_string

def search_sunlight(name_part = None, state=None):
	#TODO: Finish
	legislators = sunlight.congress.legislator_search(name_part) # legislators should be a list...