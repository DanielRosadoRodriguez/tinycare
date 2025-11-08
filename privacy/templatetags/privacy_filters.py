from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_to_html(text):
    """Convierte Markdown a HTML."""
    return mark_safe(markdown.markdown(text))
