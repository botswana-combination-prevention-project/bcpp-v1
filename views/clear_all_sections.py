from django.shortcuts import render_to_response
from django.template import RequestContext
#from bhp_mapping.helpers import get_regions
from bhp_map.exceptions import MapperError
from bhp_map.classes import mapper


def clear_all_sections(request):
    """Clears all sections for a given region."""

    template = 'clear_all_sections.html'
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        return render_to_response(
                template, {
                    'item_label': m.get_item_model_cls._meta.object_name,
                    'region_label': '{0}s'.format(m.region_label),
                    'regions': m.get_regions(),
                 },
                context_instance=RequestContext(request)
            )
