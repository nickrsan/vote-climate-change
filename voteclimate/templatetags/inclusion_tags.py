__author__ = 'Nick'

from django import template, forms
from django.db.models import Count

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

@register.inclusion_tag('top_candidates.django_include')
def top_candidates():
	candidates = models.candidate.objects.annotate(num_statements = Count('statement')).filter(num_statements__gte=1).order_by('-num_statements')[:15]
	return {'top_candidates':candidates}

@register.inclusion_tag('highlight.django_include')
def highlight(number):
	offset = number - 1
	try:
		highlight = models.statement.objects.filter(highlight = True)[offset:number][0] # limit 1
	except IndexError:
		return {'highlight':None}
	return {'highlight':highlight}

@register.inclusion_tag('stats.django_include')
def pledge_stats():
	return{'num_pledges':models.statement.objects.count()}