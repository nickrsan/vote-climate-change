from django import template, forms
from EC.feedback.models import FeedbackForm

register = template.Library()

@register.inclusion_tag('feedback_form.django_include')
def feedback_form():
    return {'form':FeedbackForm()}