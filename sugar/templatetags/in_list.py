'''
From http://www.djangosnippets.org/snippets/177/#c196 by mikeivanov
'''
from django import template
register = template.Library()

@register.filter
def in_list(value,arg):
    '''
    Usage
    {% if value|in_list:list %}
    {% endif %}
    '''
    return value in arg
