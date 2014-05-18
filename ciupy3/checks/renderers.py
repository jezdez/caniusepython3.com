import mimetypes
import requests

try:
    # Python 2
    from StringIO import StringIO as BytesIO
except ImportError:
    # Python 3
    from io import BytesIO

from rest_framework.renderers import BaseRenderer

if '.svg' not in mimetypes.types_map:
    mimetypes.add_type("image/svg+xml", ".svg")


SHIELD_URL = "http://img.shields.io/badge/%s-%s-%s.%s"


class ShieldRenderer(BaseRenderer):
    """
    All renderers should extend this class, setting the `media_type`
    and `format` attributes, and override the `.render()` method.
    """
    charset = 'utf-8'
    render_style = 'binary'
    subject = 'Python 3 port'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        request = renderer_context['request']
        if 'checks' in data:
            check = data['checks'][0]
        else:
            check = data

        if not data:
            color = 'white'
            status = 'error'
        elif check.get('finished_at', None):
            num_blockers = len(check['blockers'])
            if num_blockers == 1:
                status = '%s blocker' % num_blockers
            else:
                status = '%s blockers' % num_blockers
            if num_blockers == 0:
                color = 'brightgreen'
            elif num_blockers == check['unblocked']:
                color = 'red'
            else:
                color = 'yellow'
        else:
            color = 'lightgrey'
            status = 'unchecked'

        shield_url = SHIELD_URL % (
            self.subject,
            status,
            color,
            self.format,
        )
        if request.QUERY_PARAMS.get('style', '') == 'flat':
            shield_url += '?style=flat'
        shield_response = requests.get(shield_url)
        return shield_response.content


class SVGRenderer(ShieldRenderer):
    media_type = 'image/svg+xml'
    format = 'svg'


class PNGRenderer(ShieldRenderer):
    media_type = 'image/png'
    format = 'png'
