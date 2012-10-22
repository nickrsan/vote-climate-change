# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
from django.template.loader import render_to_string

from vote_climate import settings
import models
import utils

import simplejson
import compile_less # we want to autocompile less scripts on load
def log(msg):
	# 	TODO: needs to be fized by the time we go live

	print msg

try:
	import sunlight
except:
	log("Couldn't import sunlight")
	raise


def home(request):

	compile_less.compile_less(dirs = settings.STATICFILES_DIRS)

	# set the publisher
	common_elements = get_common_elements()

	statements = models.statement.objects.all().order_by('-id')[:100]

	template = loader.get_template("index.django")
	cont = RequestContext(request,{'title':"Vote Climate Change",
								   'publisher':common_elements['publisher'].publisher,
								   'style_id':common_elements['publisher'].id,
								   'facts':common_elements['facts'],
								   'statements':statements,
								   'pagetitle':"Climate Solutions Win Votes",
								   })

	# need RequestContext
	return HttpResponse(template.render(cont))

def rerender(request):
	#utils._fix_photo_urls(r'C:\Users\Nick\workspace\voteclimate')
	utils._rerender_statements()
	return HttpResponse("done")

def get_common_elements():

	common_elements = {}
	common_elements['publisher'] = models.style.objects.get(name="voting_for")
	common_elements['facts'] = models.fact.objects.all()[:8]
	return common_elements

def candidate(request,candidate_name = None, state = None):
	if candidate_name is None:
		return redirect("/")

	if state is None:
		possible_candidates = models.candidate.objects.filter(name__iexact = candidate_name)
	else:
		state_obj = utils.find_state(state)
		possible_candidates = models.candidate.objects.filter(name__iexact = candidate_name,state = state_obj)

	common_elements = get_common_elements()
	template = loader.get_template("index.django")

	if state:
		page_title = "%s (%s)" % (candidate_name,state)
	else:
		page_title = candidate_name

	if len(possible_candidates) == 0:

		cont = RequestContext(request,{'title':"Vote Climate Change",
									   'pagetitle':page_title,
									   'facts':common_elements['facts'],
									   'alert_msg': "No candidate with that name and state",
									   })


	for candidate in possible_candidates:
		candidate_statements = models.statement.objects.filter(candidate = candidate)
		cont = RequestContext(request,{'title':"Vote Climate Change",
									   'pagetitle':page_title,
									   'statements': candidate_statements,
									   'facts':common_elements['facts'],
									   })
	return HttpResponse(template.render(cont))


def error(request,error_string):
	# TODO: Finish this and make sure it prints correctly
	template = loader.get_template("index.django")

	cont = RequestContext(request,{'title':"Error","text":error_string})

	return HttpResponse(template.render(cont))

def fix_photos(request):

	utils._fix_photo_urls('/home/voteclimatechange/voteclimatechange.com')

	return HttpResponse("done")


def add_statement(request):

	data = None
	if request.is_ajax():
		#TODO Make this part work
		pass
	if request.POST:
		data = request.POST
	elif request.GET:
		data = request.GET

	statement_form = models.publisher_form(data,request_ip=request.META['REMOTE_ADDR'])
	if statement_form.is_valid():
		try:
			added_style = models.style.objects.get(pk=statement_form.cleaned_data['style_id'])
		except:
			added_style = 1
			# TODO: Should we fail over to a default style, or should we return an error?

		new_user = statement_form.cleaned_data['user_object']
		new_state = statement_form.cleaned_data['state']
		# next: if candidate doesn't exist - should check the existing candidates first
		# then check the sunlight api. This way it learns as people add them

		# then make a candidate record (function)

		# if it does, use it

		new_statement = models.statement(
			candidate = statement_form.cleaned_data['candidate'],
			user = new_user,
			style = added_style,
			extra_text = statement_form.cleaned_data['extra_text'],
			support_style = statement_form.cleaned_data['support_style'],
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
