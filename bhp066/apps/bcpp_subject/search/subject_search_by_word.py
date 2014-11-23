from edc.dashboard.search.classes import BaseSearchByWord

from ..models import SubjectConsent


class SubjectSearchByWord(BaseSearchByWord):

    name = 'word'
    order_by = ['-created']
    search_model = SubjectConsent
    template = 'subjectconsent_include.html'

    def contribute_to_context(self, context):
        context = super(BaseSearchByWord, self).contribute_to_context(context)
#         context.update({
#             'subject_dashboard_url': 'subject_dashboard_url'})
        return context
