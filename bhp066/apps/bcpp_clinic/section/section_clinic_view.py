from datetime import date

from django.conf import settings

from edc.device.device.classes import device
from edc.map.classes import site_mappers

from apps.bcpp_survey.models import Survey

from ..search import ClinicSearchByWord

from ..models import ClinicEligibility, DailyLog

from edc.dashboard.section.classes import BaseSectionView, site_sections


class SectionClinicView(BaseSectionView):
    section_name = 'clinic'
    section_display_name = 'Clinic Subjects'
    section_display_index = 45
    section_template = 'section_bcpp_clinic.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = ClinicEligibility
    search = {'word': ClinicSearchByWord}

    def contribute_to_context(self, context, request, *args, **kwargs):
        try:
            daily_log = DailyLog.objects.get(report_date=date.today())
        except DailyLog.DoesNotExist:
            daily_log = None
        current_survey = Survey.objects.current_survey()
        context.update({
            'current_survey': current_survey,
            'current_community': str(site_mappers.get_current_mapper()()),
            'daily_log': daily_log,
            'subject_dashboard_url': self.dashboard_url_name,
            })
        return context

# only include section for CPC or the central server
if site_mappers.get_current_mapper().intervention or device.device_id == '99':
    site_sections.register(SectionClinicView)
