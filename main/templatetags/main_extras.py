from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def url_name_scramble(value):
	return '.'.join(value.lower().split())