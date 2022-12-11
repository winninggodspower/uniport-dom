from django import template
from django.conf import settings
from django.urls import reverse

register = template.Library()

@register.filter(name='get_setting')
def settings_value(name):
    return getattr(settings, name)
