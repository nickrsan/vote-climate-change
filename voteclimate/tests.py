"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

import global_funcs

import models
import utils

class CandidateLoadTest(TestCase):
	"""
		We need a test that makes sure we get a candidate out of searching sunlight
	"""

	fixtures = ["dumped.json"]

	def setup(self):
		self.candidates = utils.search_and_merge("Pelosi")
		self.single_candidate = self.candidates[0]

	def test_candidate_loading(self):
		self.setup()
		self.assertEqual(type(self.single_candidate),models.candidate)
		self.assertEqual(self.single_candidate.name,"Nancy Pelosi") # this is probably the wrong way to write this, but it'll do for now

	def test_candidate_matching(self):
		"""
			Test that if we provide only the IDs for a candidate (the one that is already set up)
			we get back the full candidate with all details
		"""

		self.setup()

		self.fake_leg = {
			# ids for Nancy Pelosi
			'govtrack_id': '400314',
			'crp_id': 'N00007360',
			'votesmart_id':'26732',
			'fec_id':'H8CA05035',
		}
		self.fake_results = [{
			'legislator':self.fake_leg,
		}]

		candidates = utils.match_sunlight_to_db(self.fake_results)
		single_cand = candidates[0]

		self.assertEqual(single_cand.name,"Nancy Pelosi") # this is probably the wrong way to write this, but it'll do for now
		self.assertEqual(single_cand,self.single_candidate)

	def test_sunlight_short_circuit(self):
		"""
			Checks that when we search sunlight, it short circuits correctly - searches we've already made get skipped
		"""

		return_val = utils.search_sunlight("barbara boxer")
		self.assertNotEqual(None,return_val)
		second_time = utils.search_sunlight("nancy pelosi")
		self.assertNotEqual(None,second_time)
		should_be_none = utils.search_sunlight("barbara boxer")
		self.assertEqual(None,should_be_none)



class StateTest(TestCase):
	"""
		Tests the state retrieval code to make sure that each passed in item returns the correct state
	"""

	fixtures = ["dumped.json"]

	def setup(self):
		# need two states and the non-state
		self.state = models.state.objects.all()
		self.ok_state = models.state.objects.get(abbreviation="OK")
		self.ca_state = models.state.objects.get(abbreviation="CA")
		self.other_state = models.state.objects.get(abbreviation="XOT")

	def test_state_retrieval(self):

		self.setup()
		print self.ca_state.abbreviation
		retrieved_ok = utils.find_state('ok')
		self.assertEqual(self.ok_state,retrieved_ok)
		retrieved_full = utils.find_state("oklahoma")
		self.assertEqual(self.ok_state,retrieved_full)

		# make sure they aren't equal because it's always retrieving the same thing
		self.assertNotEqual(self.ca_state,retrieved_ok)

		nonexistent_state = utils.find_state('babbledie-gook')
		self.assertEqual(nonexistent_state,self.other_state)
		self.assertNotEqual(nonexistent_state,retrieved_ok)


class StripTags(TestCase):

	def setup(self):
		self.test_strings = {
			"<p><b></b><strong></strong></p>":(None,None,''), # only tags
			"<p class='notbogus'><nicktag id='hi'></nicktag><anothertag /></p>":(None,None,"<nicktag id='hi'></nicktag><anothertag />"), # bogus tags inside regular tags
			"<p class='simpleclass'>Testing text with <strong>specific</strong> strips</p>":(['strong',],None,"<p class='simpleclass'>Testing text with specific strips</p>"),
			"<p class='simpleclass'>Testing text with <strong>specific</strong> keeps</p>":(None,['strong'],"Testing text with <strong>specific</strong> keeps"),
			"<p class='simpleclass'>Testing text with <strong>specific</strong> strips and keeps</p>":(['p'],['strong'],"Testing text with <strong>specific</strong> strips and keeps"),
			"<p class='munged'>Testing munged <strong tag</p>":(None,None,'Testing munged '),
			"<p class='munged'>Testing munged <non tag</p>":(None,None,'Testing munged <non tag'),
			"<p class='munged'>Testing munged <non tag </p>":(None,['p'],"<p class='munged'>Testing munged <non tag </p>"),
		}

	def test_strip_tags(self):
		self.setup()

		for test in self.test_strings:
			self.assertEqual(global_funcs.strip_tags(test,self.test_strings[test][0],self.test_strings[test][1]),
				self.test_strings[test][2])
