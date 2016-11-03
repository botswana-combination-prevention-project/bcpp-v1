from django import template
register = template.Library()


@register.filter(name='index_dictionary')
def index_dictionary(dictionary, key):
    if key != 'None':
        return dictionary[key]
    else:
        return 'None'
