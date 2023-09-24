import markdown
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def markdown_it(value):
    return markdown.markdown(value, extensions=['markdown.extensions.fenced_code'])