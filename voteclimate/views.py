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

def error(request,error_string):
	# TODO: Finish this and make sure it prints correctly
	template = loader.get_template("index.django")

	cont = RequestContext(request,{'title':"Error","text":error_string})

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
		try:
			added_style = models.style.objects.get(pk=statement_form.cleaned_data['style_id'])
		except:
			added_style = 1
			# TODO: Should we fail over to a default style, or should we return an error?

		new_state = utils.find_state(statement_form.cleaned_data['state'])
		new_user = models.user(name = statement_form.cleaned_data['person_name'],
		                       ip = request.META['REMOTE_ADDR'])
		new_user.save()

		# next: if candidate doesn't exist - should check the existing candidates first
		# then check the sunlight api. This way it learns as people add them

		# then make a candidate record (function)

		# if it does, use it

		new_statement = models.statement(
			candidate = statement_form.cleaned_data['candidate'],
			user = new_user,
			state = new_state,
			style = added_style,
		)
		new_statement.rendered_text = render_to_string(added_style.output_template, {'statement':new_statement})
		new_statement.save()
	else:
		#TODO: Fix the error display
		for error in statement_form.errors['__all__']:
			print error
		return HttpResponse(statement_form.errors['__all__'])

	return redirect("/")

def render_statement_to_json(statement,style):
	html = render_to_string(style.output_template, statement)
	serialized_data = simplejson.dumps({"statement_html": html})
	return HttpResponse(serialized_data, mimetype="application/json")


def find_electable(request, search_string= None):

	candidates = utils.find_candidate(search_string)

	if True or request.is_ajax():

		callback = request.GET['callback']

		json_string = "%s({totalResultsCount:%s, electables:[" % (callback,len(candidates))

		for candidate in candidates:
			try:
				json_string = "%s%s," % (json_string,candidate.to_json())
			except:
				raise

		return HttpResponse("%s]});" % (json_string))
	#else:
		# this area is unreachable for now. We need to switch it over if we decide to have a true search
	#	template = loader.get_template("index.django")
	#	cont = RequestContext(request,{'title':"Find Patient - searched '%s'" % search_string,'patients': found_patients})

	#	return HttpResponse(template.render(cont))
