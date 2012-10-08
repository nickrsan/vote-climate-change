# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
from django.template.loader import render_to_string

import models
import utils

import simplejson

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
	publisher_style = models.style.objects.get(name="voting_for")

	facts = models.fact.objects.all()[:8]

	statements = models.statement.objects.all()[:100]

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

	statement_form = models.publisher_form(data)
	if statement_form.is_valid():
		added_style = models.style.objects.get(pk=statement_form.cleaned_data['style'])
		name = statement_form.cleaned_data['person_name']

		# next: if candidate doesn't exist - should check the existing candidates first
		# then check the sunlight api. This way it learns as people add them

		# then make a candidate record (function)

		# if it does, use it

		return redirect("/")

def render_statement_to_json(statement,style):
	html = render_to_string("statement.django_include", statement)
	serialized_data = simplejson.dumps({"statement_html": html})
	return HttpResponse(serialized_data, mimetype="application/json")


def find_electable(request, search_string= None):
	# TODO implement search



	return search_string
