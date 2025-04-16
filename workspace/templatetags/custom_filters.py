from django import template
import os

register = template.Library()

@register.filter
def basename(value):
    if not value:
        return "-"
    try:
        return os.path.basename(value)
    except (TypeError, AttributeError):
        return value

@register.filter
def getkey(value, key):
    try:
        return value[key]
    except (KeyError, TypeError):
        return None