from django.shortcuts import render_to_response
from django.template import RequestContext
#from bhp_mapping.helpers import get_regions
from bhp_map.exceptions import MapperError
from bhp_map.classes import site_mappers


def clear_all_sections(request, **kwargs):
    """Clears all sections for a given region."""

    template = 'clear_all_sections.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'item_label': m.get_item_label(),
                    'section_label': m.get_section_label(),
                    'region_label': '{0}s'.format(m.get_region_label()),
                    'regions': m.get_regions(),
                    'region_field_attr': m.get_region_field_attr(),
                 },
                context_instance=RequestContext(request)
            )
