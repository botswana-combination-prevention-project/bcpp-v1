from bhp_section.classes import BaseSectionView, site_sections
from models import Household


class SectionHouseholdView(BaseSectionView):
    section_name = 'household'
    section_display_name = 'Households'
    section_display_index = 10
    section_template = 'section_household.html'
    add_model = Household

site_sections.register(SectionHouseholdView)
