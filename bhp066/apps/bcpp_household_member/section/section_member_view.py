from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from apps.bcpp_household.constants import CONFIRMED

from ..search import MemberSearchByWord

site_mappers.autodiscover()


class SectionMemberView(BaseSectionView):
    section_name = 'member'
    section_display_name = 'Members'
    section_display_index = 30
    section_template = 'section_member.html'
    search = {'word': MemberSearchByWord}

    def contribute_to_context(self, context, request, *args, **kwargs):
        """Users may override to update the template context with {key, value} pairs."""
        context.update({'CONFIRMED': CONFIRMED})
        return context

site_sections.register(SectionMemberView)
