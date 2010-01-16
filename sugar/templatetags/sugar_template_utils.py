from django import template

register = template.Library()

class RenderInlineNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        source = self.nodelist.render(context)
        t = template.Template(source)
        return t.render(context)

@register.tag
def render_inline(parser, token):
    """
    Renders its contents to a string using the current context, allowing you
    to process template variables embedded in things like model content,
    django-flatblocks, etc.

    Usage:

    {% render_inline %}
    Foo

    Bar

    {{ something_with_embedded_django_template }}

    Baaz

    {% end_render_inline %}

    """

    nodelist = parser.parse(('end_render_inline',))

    parser.delete_first_token()

    return RenderInlineNode(nodelist)