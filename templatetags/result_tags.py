from django import template
from bhp_common.utils import formatted_age
register = template.Library()


@register.filter(name='result_age')
def result_age(born, collection_date):
    reference_date = collection_date.date()
    return formatted_age(born, reference_date)


@register.filter(name='result_clinic_name')
def result_clinic_name(site_identifier, protocol_identifier):

    site_name = None

    """
    if Protocol.objects.filter(protocol_identifier__iexact=protocol_identifier):
        oProtocol = Protocol.objects.get(protocol_identifier__iexact=protocol_identifier)
        for site in oProtocol.site.all():
            if site.site_identifier == site_identifier:
                site_name = '%s %s %s' % (site_identifier, oProtocol.site_name_fragment, site.location)
    """

    if not site_name:
        site_name = site_identifier
    return site_name


@register.filter(name='filter_validation_by_status')
def filter_validation_by_status(value, status):
    if status == 'R':
        return 'Rejected'
    elif status == 'P':
        return 'Preliminary'
    else:
        return value


@register.filter(name='status_flag')
def status_flag(value):
    if value == 'F':
        return ''
    else:
        return value


@register.filter(name='hide_not_final')
def hide_not_final(value, validation_status):
    if validation_status == 'F':
        return value
    else:
        return '****'


@register.filter(name='quantifier')
def quantifier(value):
    if value == '=':
        return ''
    else:
        return value
