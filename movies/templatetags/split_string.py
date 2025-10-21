from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
  """
    Returns the first value split from certain key.
  """
  return value.split(key)[0]