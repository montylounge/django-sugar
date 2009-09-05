from django.views.debug import technical_500_response
import sys
from django.conf import settings

class UserBasedExceptionMiddleware(object):
    """
    Source: http://ericholscher.com/blog/2008/nov/15/debugging-django-production-environments/

    Introduction
    ------------
    This is a pretty simple middleware that is crazy useful. When you throw this
    inside of your site, it will give you a normal Django error page if
    you're a superuser, or if your IP is in INTERNAL_IPS.

    Implement
    ---------
    Add to your middleware:

    'sugar.middleware.debugging.UserBasedExceptionMiddleware',

    """

    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())