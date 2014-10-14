from ..search import ClinicSearchByWord

from ..models import ClinicEligibility

from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections


class SectionClinicView(BaseSectionForDashboardView):
    section_name = 'subject'
    section_display_name = 'Clinic Subjects'
    section_display_index = 40
    section_template = 'section_bcpp_clinic.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = ClinicEligibility
    search = {'word': ClinicSearchByWord}
site_sections.register(SectionClinicView)
