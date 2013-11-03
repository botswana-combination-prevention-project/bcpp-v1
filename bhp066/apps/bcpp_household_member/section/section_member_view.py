from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from ..search import MemberSearchByWord

site_mappers.autodiscover()


class SectionMemberView(BaseSectionView):
    section_name = 'member'
    section_display_name = 'Members'
    #add_model = HouseholdMember
    section_display_index = 30
    section_template = 'section_member.html'
    search = [MemberSearchByWord]

site_sections.register(SectionMemberView)
