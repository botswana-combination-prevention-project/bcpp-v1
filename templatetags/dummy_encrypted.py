from django import template

register = template.Library()


@register.filter(name='encrypted')
def encrypted(value):
    return value
