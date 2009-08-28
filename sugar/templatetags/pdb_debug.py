"""
Source: http://www.djangosnippets.org/snippets/1550/ 

Notes
=====
This allows you to set up a breakpoint anywhere in your template code, 
by simply writing {% pdb_debug %}.

You can then access your context variables using context.get(..) at the pdb 
prompt. Optionally, install the ipdb package for colors, completion, and more (easy_install ipdb).

"""

from django.template import Library, Node

register = Library()

try:
    import ipdb as pdb
except ImportError:   
    import pdb

class PdbNode(Node):
    def render(self, context):
        pdb.set_trace()
        return ''

@register.tag
def pdb_debug(parser, token):
    return PdbNode()
