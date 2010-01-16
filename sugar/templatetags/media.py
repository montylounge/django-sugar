from django.template import Library, Node
from django.template.loader import render_to_string
from django.contrib.sites.models import Site    
from django.conf import settings
import os, urlparse
     
register = Library()
     
def _absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    domain = Site.objects.get_current().domain
    return 'http://%s%s' % (domain, url)

@register.simple_tag
def media(filename, flags=''):
    """
     Autor: http://softwaremaniacs.org/blog/2009/03/22/media-tag/
    
    {% load media %}
    <link rel="stylesheet" href="{% media "css/style.css" %}">
    
    {% media "css/style.css" %}                <!-- ...style.css?123456789 -->
    {% media "css/style.css" "no-timestamp" %} <!-- ...style.css -->
    {% media "images/edit.png" "timestamp" %}  <!-- ...edit.png?123456789 -->
    {% media "images/edit.png" "absolute" %} <!-- http://example.com/media/edit.png -->
    """
    flags = set(f.strip() for f in flags.split(','))
    url = urlparse.urljoin(settings.MEDIA_URL, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
       'timestamp' in flags:
        fullname = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url