from django import template

register = template.Library()

@register.filter(name='titlify')
def titlify(value):
    """Prepends value and emdash to base title"""
    title_base = 'Platform Cooperatives Worldwide'
    return value + ' – ' + title_base
