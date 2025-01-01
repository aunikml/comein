from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return value * arg
    except:
        return ""

@register.filter
def div(value, arg):
     try:
        return value / arg
     except:
        return ""
@register.filter
def getkey(value, arg):
    """Retrieves a value from a dictionary using a key"""
    try:
        return value[arg]
    except (KeyError, TypeError):
        return ''