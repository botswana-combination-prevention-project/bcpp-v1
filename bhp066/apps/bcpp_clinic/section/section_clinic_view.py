from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections

from ..search import ClinicSearchByWord

from ..models import ClinicConsent


class SectionClinicView(BaseSectionForDashboardView):
    section_name = 'clinic'
    section_display_name = 'Clinic Subjects'
    section_display_index = 60
    section_template = 'section_bcpp_clinic.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = ClinicConsent
    search = [ClinicSearchByWord]
site_sections.register(SectionClinicView)
