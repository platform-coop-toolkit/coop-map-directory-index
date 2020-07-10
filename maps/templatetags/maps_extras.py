import datetime
import json
from decimal import Decimal
from django import template
from django import template
from django.conf import settings
from django.http import QueryDict
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

register = template.Library()

ISO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

# From: https://gist.github.com/czue/90e287c9818ae726f73f5850c1b00f7f


def json_handler(obj):
    if callable(getattr(obj, 'to_json', None)):
        return obj.to_json()
    elif isinstance(obj, datetime.datetime):
        return obj.strftime(ISO_DATETIME_FORMAT)
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, datetime.time):
        return obj.strftime('%H:%M:%S')
    elif isinstance(obj, Decimal):
        return float(obj)  # warning, potential loss of precision
    elif isinstance(obj, Promise):
        return force_str(obj)  # to support ugettext_lazy
    else:
        return json.JSONEncoder().default(obj)


@register.filter(name='titlify')
def titlify(value):
    """Prepends value and emdash to base title"""
    title_base = 'Platform Co-op Directory'
    return value + ' – ' + title_base

# From: https://gist.github.com/czue/90e287c9818ae726f73f5850c1b00f7f


@register.filter
def to_json(obj):
    def escape_script_tags(unsafe_str):
        # seriously: http://stackoverflow.com/a/1068548/8207
        return unsafe_str.replace('</script>', '<" + "/script>')

    # json.dumps does not properly convert QueryDict array parameter to json
    if isinstance(obj, QueryDict):
        obj = dict(obj)
    # apply formatting in debug mode for ease of development
    indent = None
    if settings.DEBUG:
        indent = 2
    return mark_safe(escape_script_tags(json.dumps(obj, default=json_handler, indent=indent)))


@register.inclusion_tag('maps/partials/icon.html')
def icon(name, **kwargs):
    modifier = kwargs.get('modifier', name)
    return {
        'name': name,
        'modifier': modifier,
        'size': kwargs.get('size', None),
        'ariahidden': kwargs.get('ariahidden', 'true'),
        'focusable': kwargs.get('focusable', 'false'),
        'viewbox': kwargs.get('viewbox', '0 0 20 20'),
        'class_override': kwargs.get('class_override', None)
    }
