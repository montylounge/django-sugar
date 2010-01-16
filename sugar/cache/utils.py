import re

try:
    from hashlib import md5
except ImportError:
    import md5


from django.db.models.manager import Manager
from django.utils.encoding import smart_str


def clean_cache_key(key):
    '''Replace spaces with '-' and hash if length is greater than 250.'''

    #logic below borrowed from http://richwklein.com/2009/08/04/improving-django-cache-part-ii/ 
    cache_key = re.sub(r'\s+', '-', key)
    cache_key = smart_str(cache_key)

    if len(cache_key) > 250:
        m = md5()
        m.update(cache_key)
        cache_key = cache_key[:200] + '-' + m.hexdigest()

    return cache_key

def create_cache_key(klass, field=None, field_value=None):
    '''
    Helper to generate standard cache keys.

    Concepts borrowed from mmalone's django-caching:
    http://github.com/mmalone/django-caching/blob/ef7dd47e9beff39496e6a28ae129bae1b5f9ed71/app/managers.py

    Required Arguments
    ------------------
        'klass'
            Model or Manager

        'field'
            string, the specific Model field name used to create a more
            specific cache key. If you specify a field, it is used for the
            lookup to grab the value.

         'field_value'
            value, unique value used to generate a distinct key. Often
            this will be the ID, slug, name, etc.

            *Note: could be optimized/restricted to pk lookup only

    Returns
    -------
        'key'
            The key name.

    Example
    --------
        >> from blog.models import Post
        >> slug_val = 'test-foo'
        >> mykey = create_cache_key(Post, 'slug', slug_val)
        >> obj = cache.get(mykey)
    '''

    key_model = "%s.%s.%s:%s"
    key = ''

    if field and field_value:
        if isinstance(klass, Manager):
            key = key_model % (klass.model._meta.app_label, klass.model._meta.module_name, field, field_value)
        else:
            key = key_model % (klass._meta.app_label, klass._meta.module_name, field, field_value)

    if not key:
        raise Exception('Cache key cannot be empty.')

    return clean_cache_key(key)