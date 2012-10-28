__author__ = 'Nick'

from django import template, forms
from vote_climate import settings
from voteclimate import models


register = template.Library()

@register.simple_tag
def global_var(name):
	try:
		return getattr(settings,name)
	except AttributeError: # return nothing instead of crashing
		return ""

@register.inclusion_tag('facts.django_include')
def facts_box():
	all_facts = models.fact.objects.all()[:8]
	return {'facts':all_facts}