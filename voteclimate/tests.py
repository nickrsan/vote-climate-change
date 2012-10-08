"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

import global_funcs

import models
import utils

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
