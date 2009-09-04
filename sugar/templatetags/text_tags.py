from django import template

register = template.Library()

@register.filter
def truncchar(value, arg):
    '''
    Truncate after a certain number of characters.

    Source: http://www.djangosnippets.org/snippets/194/

    Notes
    -----
    Super stripped down filter to truncate after a certain number of letters.

    Example
    -------

    {{ long_blurb|truncchar:20 }}

    The above will display 20 characters of the long blurb followed by "..."

    '''

    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'