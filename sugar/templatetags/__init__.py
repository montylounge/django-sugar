# -*- mode: python; coding: utf-8; -*-

from django.template.context import Context
from functools import wraps

def private_context(f):
    """
    Simple decorator which avoids the need to a) copy-and-paste code to force
    context variables into inclusion_tag templates and b) carefully avoid
    inclusion tag variables conflicting with global variables.
    
    Instead each inclusion tag will be called with a *copy* of the provided
    context variable and its results will be merged in to avoid leaking into
    the global context

    Django's standard inclusion_tag doesn't include context variables by 
    default. When you add takes_context you are required to manually merge the 
    context variables into the dict which your tag returns, which tends to 
    result in wasteful code or accidentally leaking variables into the global 
    context with something like context.update() or name collisions.

    This decorator allows your inclusion tag to remain simple and still have 
    safe access to the global context for things like MEDIA_URL:

    @register.inclusion_tag('my_template')
    @private_context
    def my_tag(context, …):
      return {"foo": 1, "bar": 2}

    See:
    http://www.djangosnippets.org/snippets/1687/
    
    """
    
    @wraps(f)
    def private_context_wrapper(context, *args, **kwargs):
        c = Context(context)
        rc = f(c, *args, **kwargs)
        c.update(rc)
        return c

    return private_context_wrapper