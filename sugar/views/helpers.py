# -*- mode: python; coding: utf-8; -*-

from urlparse import urlsplit, urlunsplit

from django.core.urlresolvers import reverse as _reverse
from django.shortcuts import _get_queryset, get_object_or_404
from django.http import Http404
from django.contrib.sites.models import Site

from sugar.views.exceptions import Ajax404

def reverse(view_name, *args, **kwargs):
    return _reverse(view_name, args=args, kwargs=kwargs)


def absolutize_uri(request, local_url):
    request_url = urlsplit(request.build_absolute_uri(local_url))
    absolute_url = urlunsplit(request_url[:1] + (Site.objects.get_current().domain,) + request_url[2:])
    return absolute_url


def get_object_or_404_ajax(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404, e:
        raise Ajax404, e


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
