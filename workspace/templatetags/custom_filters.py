from django import template

register = template.Library()

@register.filter
def getkey(dictionary, key):
    """Get the value from a dictionary using a key."""
    try:
        return dictionary.get(key, None)
    except AttributeError:
        return None
