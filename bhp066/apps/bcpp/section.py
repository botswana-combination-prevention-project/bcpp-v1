from collections import namedtuple

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.device.device.classes import Device

ModelMeta = namedtuple('ModelMeta', 'app_label model_name')


class SectionAdministrationView(BaseSectionView):
    section_name = 'administration'
    section_display_name = 'Administration'
    section_display_index = 140
    section_template = 'bcpp_section_administration.html'

    def contribute_to_context(self, context, request, *args, **kwargs):
        context.update({
            'is_server': Device().is_server,
            'replaceable_meta': ModelMeta('bcpp_household', 'replaceable'),
            'plot_meta': ModelMeta('bcpp_household', 'plot'),
            'household_meta': ModelMeta('bcpp_household', 'household'),
            'subjectconsent_meta': ModelMeta('bcpp_subject', 'subjectconsent'),
            })
        return context

site_sections.register(SectionAdministrationView, replaces='administration')
