from django import template
from django.urls import reverse
from ..utils import is_user_online

register = template.Library()


@register.filter(name='join')
def join(arg1, arg2):
    return ''.join([str(arg1), str(arg2)])


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    url_copy = context['request'].GET.copy()
    for key, word in kwargs.items():
        url_copy[key] = word
    return url_copy.urlencode()


@register.simple_tag(name='redirect')
def url_redirect(url):
    return reverse(url)


@register.simple_tag(name='is_user_online')
def _is_user_online(user):
    if is_user_online(user):
        return '#0f0'
    return '#f00'
