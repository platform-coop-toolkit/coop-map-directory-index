from django import template
from accounts.models import SocialNetwork

register = template.Library()


@register.filter(name='titlify')
def titlify(value):
    """Prepends value and emdash to base title"""
    title_base = 'Platform Co-op Directory'
    return value + ' – ' + title_base


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
