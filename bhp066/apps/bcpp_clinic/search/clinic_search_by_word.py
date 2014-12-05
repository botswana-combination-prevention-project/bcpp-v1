from ..models import ClinicEligibility

from edc.dashboard.search.classes import BaseSearchByWord


class ClinicSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = ClinicEligibility
    order_by = ['-created']
    template = 'cliniceligibility_include.html'

    def contribute_to_context(self, context):
        context = super(BaseSearchByWord, self).contribute_to_context(context)
        context.update({
            'subject_dashboard_url': 'subject_dashboard_url'},
             clinic_eligibility_meta=ClinicEligibility._meta,)
        return context
