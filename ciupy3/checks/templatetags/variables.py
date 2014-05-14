from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set(context, *args, **kwargs):
    if args:
        raise template.TemplateSyntaxError("'set' tag doesn't "
                                           "take positional arguments")
    for key, value in kwargs.items():
        context[key] = value
    return ''


@register.tag
def capture(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'capture' node requires a variable name.")
    nodelist = parser.parse(('endcapture',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output.strip()
        return ''
