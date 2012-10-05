# Create your views here.

from django.shortcuts import render_to_response

from models import statement, fact

def log(msg):
	# 	TODO: needs to be fized by the time we go live

	print msg

try:
	import sunlight
except:
	log("Couldn't import sunlight")
	raise


def home(request):

	facts = fact.objects.all()

	return render_to_response("index.django", {'title':"Vote Climate Change",'publisher':"publisher_voting_for.django",'facts':facts})