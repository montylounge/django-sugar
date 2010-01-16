# -*- mode: python; coding: utf-8; -*-

""" Custom exceptions """

class AjaxException(Exception):
    """Base class for AJAX exceptions"""
    pass

class Ajax404(AjaxException):
    """Object not found"""
    pass

class AjaxDataException(AjaxException):
    """
    Use it to push json data to response
    """

    def __init__(self, data, *args, **kwargs):
        self.data = data
        Exception.__init__(self, *args, **kwargs)

class RedirectException(Exception):
    def __init__(self, redirect_uri, *args, **kwargs):
        self.redirect_uri = redirect_uri
        self.notice_message = kwargs.pop('notice_message', None)
        self.error_message = kwargs.pop('error_message', None)
        Exception.__init__(self, *args, **kwargs)