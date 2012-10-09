from django.db.models import Q

import views
import models
import sunlight


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

	if not search_str and request:
		try:
			search_str = request.GET['candidate_find']
		except:
			pass

	if not search_str:
		raise ValueError("No search string provided")

	# split all of the words, we'll search for each word in the first name and last name fields and only
	# return patients who have a match for each word
	strings = search_str.split(" ")

	tQ = Q(name__contains=strings[0]) # initialize the Q object by searching for the first string

	for t_str in strings[1:]: # now compose the rest of it by searching for each string in first/last name fields and & with the other requirements
		tQ = tQ & Q(name__contains=t_str)

	# now pass the Q object in for the search
	found_candidates = models.candidate.objects.filter(tQ)
	return found_candidates

def find_candidate(search_str,request=None):
	return search_and_merge(search_str)

def search_and_merge(name_string):
	if len(name_string) > 4:
		# don't search if it's too short. Waste of resources because it won't return anything
		sunlight_data = search_sunlight(name_string)
		new_list = match_sunlight_to_db(sunlight_data)

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


def match_sunlight_to_db(sunlight_results):

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

	for legislator in sunlight_results:
		legislator = legislator['legislator'] # need to get the subkey and overwrite - it's a subdictionary
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

def add_statement_to_db(name,state,text,style_id,candidate_text):

#strip tags on everything

	pass

def isiterable(item):
	'''tests whether an object is iterable'''
	if hasattr(item,'__iter__'):
		return True
	else:
		return False
