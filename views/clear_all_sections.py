from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_mapping.helpers import get_regions


def clear_all_sections(request):
    """Clears all sections for a given region."""

    template = 'clear_all_sections.html'
    region_label = 'wards'
    item_label = 'household'
    return render_to_response(
            template, {
                'item_label': item_label,
                'region_label': region_label,
                'regions': get_regions(),
             },
            context_instance=RequestContext(request)
        )
