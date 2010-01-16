from django.core.paginator import Paginator
from django import template

register = template.Library()

class PaginatorNode(template.Node):
    """
    templatetag for paginating any iterable template variable (queryset, list, etc.)

    Assume that the query string provided has a key "page" containing the current page

    Usage:

        {% paginate list_of_documents request.GET %}
            <ul class="children">
            {% for doc in page.object_list %}
                <li>
                    <h2><a href="{{ doc.get_absolute_url }}">{{ doc.title }}</a></h2>
                    {{ doc.summary }}
                </li>
            {% endfor %}
            </ul>
        {% endpaginate %}
    """

    def __init__(self, nodelist, objects=None, query_string=None, page_size=10):
        self.nodelist = nodelist
        self.objects = template.Variable(objects)
        self.query_string = template.Variable(query_string)
        self.page_size = page_size

    def render(self, context):
        ctx = template.Context(context)

        objects = self.objects.resolve(ctx)
        query_string = self.query_string.resolve(ctx)

        paginator = Paginator(objects, self.page_size)

        page = 1
        if 'page' in query_string:
            try:
                page = int(query_string['page'])
            except ValueError:
                pass

        page = min(page, paginator.num_pages)

        ctx.update({
            "paginator":    paginator,
            "page_number":  page,
            "page":         paginator.page(page)
        })

        return self.nodelist.render(ctx)


    @classmethod
    def paginate_tag(cls, parser, token):
        args = token.contents.split()

        if not len(args) >= 3:
            raise template.TemplateSyntaxError, "%r tag must be called like this: {% paginate queryset_or_iterable query_string [page_size] %}" % args[0]

        nodelist = parser.parse(('endpaginate',))

        parser.delete_first_token()

        kwargs = {
            "objects": args[1],
            "query_string": args[2],
        }

        if len(args) > 3:
            kwargs['page_size'] = int(args[3])

        return PaginatorNode(nodelist, **kwargs)

register.tag("paginate", PaginatorNode.paginate_tag)