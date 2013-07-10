from bhp_section.classes import BaseSectionView, site_sections
from bhp_map.classes import site_mapper
from models import Household
from forms import CommunityForm


site_mapper.autodiscover()


class SectionHouseholdView(BaseSectionView):
    section_name = 'household'
    section_display_name = 'Households'
    section_display_index = 10
    section_template = 'section_household.html'
    add_model = Household

    def contribute_to_context(self, context):
        community_form = CommunityForm()
        context.update({'community_form': community_form})
        return context

site_sections.register(SectionHouseholdView)
