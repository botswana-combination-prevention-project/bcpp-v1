from edc.dashboard.search.classes import BaseSearchByWord

from ..models import ClinicConsent


class ClinicSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = ClinicConsent
    order_by = '-created'
    template = 'clinicconsent_include.html'

    def contribute_to_context(self, context):
        context = super(BaseSearchByWord, self).contribute_to_context(context)
        context.update({
            'subject_dashboard_url': 'subject_dashboard_url'})
        return context
