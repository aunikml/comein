from django import template
import os

register = template.Library()

@register.filter
def getkey(value, key):
    try:
        return value[key]
    except (KeyError, TypeError):
        return None

@register.filter
def basename(value):
    if value:
        return os.path.basename(str(value))
    return ''