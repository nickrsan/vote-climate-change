import os
from string import Template

from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.flatpages.models import FlatPage

import views
import models
from vote_climate import settings

import sunlight
import simplejson
import twitter_patched as twitter

twitter_api  = twitter.Api(
	consumer_key = settings.twitter_consumer_key,
	consumer_secret = settings.twitter_consumer_secret,
	access_token_key = settings.twitter_access_token_key,
	access_token_secret = settings.twitter_access_token_secret
)

class submit_response:
	def __init__(self):
		self.status = None
		self.data = None
		self.long_message = None

	def to_json(self):
		return simplejson.dumps({
		'status': self.status,
		'data': self.data,
		'long_message': self.long_message,
		})

def find_state(abbrev):
	"""
		Given a state abbreviation, it returns the state object
	"""
	try:
		return models.state.objects.get(abbreviation__iexact=abbrev) # case insensitive match
	except models.state.DoesNotExist:
		try:
			return models.state.objects.get(name__iexact=abbrev) # see if maybe it was the name - also case insensitive
		except models.state.DoesNotExist:
			return models.state.objects.get(abbreviation="XOT") # XOT is a special case

def search_only_candidate(search_str,request = None):
	"""
		Finds a candidate based upon name. request can be provided as an optional backup (not implemented)
	"""

	if request and not search_str:
		try:
			search_str = request.GET['candidate_find']
		except:
			pass

	if not search_str:
		raise ValueError("No search string provided")

	# split all of the words, we'll search for each word in the first name and last name fields and only
	# return patients who have a match for each word

	search_str = search_str.replace("%20"," ") # TODO: This is a HACK - should have to do this...
	strings = search_str.split(" ")

	tQ = Q(name__contains=strings[0]) # initialize the Q object by searching for the first string

	for t_str in strings[1:]: # now compose the rest of it by searching for each string in first/last name fields and & with the other requirements
		tQ = tQ & Q(name__contains=t_str)

	# now pass the Q object in for the search
	found_candidates = models.candidate.objects.filter(tQ).order_by('name')
	return found_candidates

def find_candidate(search_str,request=None):
	return search_and_merge(search_str)

def search_and_merge(name_string):

	# commented out the searching for now because we bring in a dump and this will make it faster
	#if len(name_string) > 4:
		# don't search if it's too short. Waste of resources because it won't return anything
	#	sunlight_data = search_sunlight(name_string)
	#	new_list = match_sunlight_to_db(sunlight_data)

	found_candidates = search_only_candidate(name_string)
	#print "found %s candidates" % len(found_candidates)
	return found_candidates


def search_sunlight(name_part = None, state=None):

	if not name_part:
		return None

	already_searched = check_and_track_sunlight_search(name_part)

	if already_searched:
		return None

	try:
		return sunlight.congress.legislator_search(name_part, all_legislators=True) # legislators should be a list...
	except:
		return [] # just play it cool

def check_and_track_sunlight_search(search_string):
	try:
		search_item = models.sunlight_search.objects.get(search=search_string)
	except models.sunlight_search.DoesNotExist:
		new_search = models.sunlight_search(search=search_string)
		new_search.save() # save the new search so we find it in the future
		return False

	return True


def fill_missing_keys(lookup, keys):
	for key in keys: #
		if not key in lookup:  # check the key
			lookup[key] = None # define it if it didn't exist



def match_sunlight_to_db(sunlight_results, mode="search"):

	#get in_offfice and order by that
	# save the webform url
	# get our own id and add it in
	# return the name, url, and our own id to the user

	# match_ids = ("govtrack_id","crp_id","votesmart_id") # more a reference than anything
	return_candidates = []
	if not sunlight_results:
		return None
	if not isiterable(sunlight_results):
		sunlight_results = [sunlight_results] # make it iterable to use the next block

	missing_keys = ('firstname','webform','bioguide_id','district','senate_class','gender','lastname','state','party','nimsp_candidate_id','votesmart_id','govtrack_id','crp_id','fec_id')
	for legislator in sunlight_results:
		if mode == "search": # from the searches, we get it back as a subkey - otherwise, it's just there in each item
			legislator = legislator['legislator'] # need to get the subkey and overwrite - it's a subdictionary

		fill_missing_keys(legislator,missing_keys)

		try:
			db_legislator = models.candidate.objects.get(
				govtrack_id = legislator['govtrack_id'],
				crp_id = legislator['crp_id'],
				votesmart_id = legislator['votesmart_id'],
				fec_id = legislator['fec_id'],
			)
			return_candidates.append(db_legislator)
		except models.candidate.DoesNotExist:
			# ok, it doesn't already exist - create it then
			new_candidate = models.candidate(
				name = "%s %s" % (legislator['firstname'],legislator['lastname']),
				state = find_state(legislator['state']),
				webform_url = legislator['webform'],
				district = legislator['district'],
				senate_class = legislator['senate_class'],
				party = legislator['party'],
			    gender = legislator['gender'],

				bioguide_id = legislator['bioguide_id'],
				fec_id = legislator['fec_id'],
				crp_id = legislator['crp_id'],
				votesmart_id = legislator['votesmart_id'],
				govtrack_id = legislator['govtrack_id'],

			    twitter_handle = legislator['twitter_id'],
			    congresspedia_url = legislator['congresspedia_url'],
			)
			new_candidate.save()
			return_candidates.append(new_candidate)
	return return_candidates

def _load_openstates(active=False):
	"""
		Loads all data from openstates into our db and caches it
	"""
	all_state_leg = sunlight.openstates.legislators(active=active,country='us')
	print "Found %s openstates candidates" % len(all_state_leg)
	match_openstates_to_db(all_state_leg)

def _load_congress(active=False):
	"""
		Loads all data from congressapi into our db and caches it
	"""
	active = not active # invert the logic because this flag is whether to include all or not
	all_congress_leg = sunlight.congress.legislators(all_legislators=active)
	print "Found %s congressional candidates" % len(all_congress_leg)
	match_sunlight_to_db(all_congress_leg,mode="load")

def match_openstates_to_db(results,return_added = False):

	return_candidates =[]

	missing_keys = ('level','url','bioguide_id','photo_url','party','nimsp_candidate_id','votesmart_id','leg_id','transparencydata_id',)

	for legislator in results:
		# check the following keys to make sure they are defined, even if None
		fill_missing_keys(legislator,missing_keys)

		if 'party' in legislator and legislator['party'] is not None:
			party = legislator['party'][0] # just the first char
		else:
			party = None

		try:

			db_legislator = models.candidate.objects.get(
				nimsp_id = legislator['nimsp_candidate_id'],
				leg_id = legislator['leg_id'],
				votesmart_id = legislator['votesmart_id'],
				transparencydata_id = legislator['transparencydata_id'],
			)
			return_candidates.append(db_legislator)
		except models.candidate.DoesNotExist:

			new_candidate = models.candidate(
				name = legislator['full_name'],
				state = find_state(legislator['state']),
				level = legislator['level'],

				webform_url = legislator['url'],
				party = party,

				bioguide_id = legislator['bioguide_id'],
				nimsp_id = legislator['nimsp_candidate_id'],
				leg_id = legislator['leg_id'],
				votesmart_id = legislator['votesmart_id'],
				transparencydata_id = legislator['transparencydata_id'],

				photo_url = legislator['photo_url']
			)

			new_candidate.save()
			if return_added:
				return_candidates.append(new_candidate)
	return return_candidates

def add_statement_to_db(name,state,text,style_id,candidate_text):

#strip tags on everything

	pass

def isiterable(item):
	'''tests whether an object is iterable'''
	if hasattr(item,'__iter__'):
		return True
	else:
		return False


def find_or_make_candidate(candidate_name, user_object):
	candidate_object = find_candidate(candidate_name)
	if candidate_object is None or len(candidate_object) == 0:
		candidate_object = make_candidate(candidate_name, user_object)
		if candidate_object is None or len(candidate_object) == 0:
			# it's still None?? balls.
			raise LookupError("Couldn't find or make a candidate")
	return candidate_object

def make_candidate(candidate_name, user_object):
	new_candidate = models.candidate(name=candidate_name,user_submitted = True,submitted_by = user_object,unconfirmed=True)
	new_candidate.save()
	return new_candidate

def find_or_make_user(user_name,user_ip,user_state):

	try:
		new_user = models.user.objects.get(name=user_name,state=user_state,ip=user_ip)
	except models.user.DoesNotExist:
		new_user = models.user(name=user_name,state=user_state,ip=user_ip)
		new_user.save()

	return new_user

def _fix_photo_urls(base_folder):
	candidates = models.candidate.objects.all()
	photo_folder = os.path.join(base_folder,"public","static","img","congress","100x125")
	for candidate in candidates:
		photo_loc = os.path.join(photo_folder,"%s.jpg" % candidate.bioguide_id)
		if candidate.bioguide_id and os.path.exists(photo_loc):
			candidate.photo_url = "/static/img/congress/100x125/%s.jpg" % candidate.bioguide_id
			candidate.save()
		else:
			candidate.photo_url = "/static/img/congress/100x125/null.jpg"
			candidate.save()

def tweet_statement(statement):
	global twitter_api

	tweet_status = statement.tweet_string

	status = twitter_api.PostUpdate(tweet_status)

def render_tweet(statement):
	if statement.candidate.twitter_handle is None: # if they don't have a twitter handle
		twitter_handle = statement.candidate.name # then just use their name
	else:
		twitter_handle = statement.candidate.twitter_handle
		if twitter_handle[0] != "@": # if it doesn't already start with an @
			twitter_handle = "@%s" % twitter_handle # then put it in

	field_map = {
		'handle':twitter_handle,
		'name':statement.user.name,
		'support_type': statement.support_short,
	}

	print statement.support_short
	print field_map['support_type']

	if statement.user.state.abbreviation != "XOT": # add state to the field map if we have it
		field_map['state'] = "in %s" % statement.user.state.abbreviation
	else:
		field_map['state'] = ""

	link = "http://voteclimatechange.com/statement/%s" % statement.id

	max_len = 140 - settings.TCO_LENGTH - 1 # -1 at end is for the space between the tweet and the link

	template = Template(statement.style.twitter_template)
	tweet_str = template.safe_substitute(**field_map)

	if len(tweet_str) > max_len: # if it's too long, then make something we're sure is short enough
		tweet_str = ".%s, you've got votes! %s" % (statement.candidate.twitter_handle,link)
	else: # we're in bounds, just append the link
		tweet_str = "%s %s" % (tweet_str,link)

	print tweet_str
	statement.tweet_string = tweet_str


def _rerender_statements():
	statements = models.statement.objects.all()
	for statement in statements:
		statement.rendered_text = render_to_string(statement.style.output_template, {'statement':statement})
		statement.save()

def make_acknowledgements_page():
	ack_page = FlatPage(title="Acknowledgements")
	ack_page.url = '/acknowledgements/'
	ack_page.template_name = 'flat_page.django'
	ack_page.enable_comments = False
	ack_page.registration_required = False
	ack_page.content = """
		We would like to acknowledge the following:

	"""
	ack_page.save()
	ack_page.sites = (1,)
	ack_page.save()

def remove_acknowledgements_page(url="/acknowledgements/"):
	ack_pages = FlatPage.objects.filter(url=url)
	for page in ack_pages:
		page.delete()

def _highlight_statement(statement_id):
	statement = models.statement.objects.get(pk = statement_id)
	statement.highlight = True
	statement.save()

def _unhighlight_statement(statement_id):
	statement = models.statement.objects.get(pk = statement_id)
	if statement.highlight is False:
		return False
	statement.highlight = False
	statement.save()
	return True
