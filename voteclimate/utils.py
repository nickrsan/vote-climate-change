import models

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

def find_candidate(name, state):
	"""
		Finds a candidate based upon name
	"""

	pass


def search_and_merge(name_part=None):
	sunlight_data = search_sunlight(name_part)
	new_queryset = match_sunlight_to_db(sunlight_data)

	return new_queryset

def search_sunlight(name_part = None, state=None):

	if not name_part:
		return None

	try:
		return sunlight.congress.legislator_search(name_part, all_legislators=True) # legislators should be a list...
	except:
		return [] # just play it cool

def match_sunlight_to_db(sunlight_results):

	#get in_offfice and order by that
	# match the ids
	# save the webform url
	# get our own id and add it in
	# return the name, url, and our own id to the user

	# match_ids = ("govtrack_id","crp_id","votesmart_id") # more a reference than anything
	return_candidates = []
	for legislator in sunlight_results:
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
				name = "%s %s" % (legislator['first_name'],legislator['last_name']),
				state = '',
				webform_url = '',
				district = '',
				senate_class = '',
				webform_url = '',
				party = '',

				fec_id = '',
				crp_id = '',
				votesmart_id = '',
				govtrack_id = '',
			)


			pass

		# everything is in dict format, look up multiple ids?
		# starting with FEC?
		pass

	pass

def add_statement_to_db(name,state,text,style_id,candidate_text):

#strip tags on everything

