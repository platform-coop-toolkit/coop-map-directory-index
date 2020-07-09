from django import template
from accounts.models import SocialNetwork

register = template.Library()


@register.filter(name='titlify')
def titlify(value):
    """Prepends value and emdash to base title"""
    title_base = 'Platform Co-op Directory'
    return value + ' – ' + title_base


@register.filter(name='social_network_id_to_label')
def social_network_id_to_label(id):
    """Takes a Social Network instance ID and returns the label"""
    sn = SocialNetwork.objects.get(id=id)
    if sn:
        return sn.name
    else:
        return None


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
