import re
from django.conf import settings
from django.utils.encoding import smart_str

_END_BODY_RE = re.compile(r'<body([^<]*)>', re.IGNORECASE)
AWESOMENESS = '<div id="awesome" style="position: fixed; bottom: 10px; right: 15px; width: 200px; height: 60px; z-index: 9000;"><a href="http://djangopony.com/" class="ponybadge" border="0" title="Magic! Ponies! Django! Whee!"><img src="http://media.djangopony.com/img/small/badge.png" width="210" height="65" alt="ponybadge"></a></div>'

class AwesomeMiddleware(object):
    """
    Middleware that makes your django application awesome.

    Implement
    ---------
    Add to your middleware:

    'sugar.middleware.awesome.AwesomeMiddleware',

    """

    def __init__(self):
        self.is_awesome = True

        #yes, you can override with your own awesomeness.
        self.awesomeness = getattr(settings, 'AWESOMENESS', AWESOMENESS)

    def __process_awesome_response(self, request, response):
        """
        Handles rendering the awesome.

        Private access because not everyone method can be this awesome.

        """
        response.content = _END_BODY_RE.sub(smart_str('<body\\1>' + self.awesomeness), response.content)
        return response

    def process_response(self, request, response):
        """
        The out-of-the-box "process_response" method isn't awesome enough,
        so we hand it off to the private _process_awesome_response method which
        is obviously much more awesome than "process_response"

        """
        return self.__process_awesome_response(request, response)