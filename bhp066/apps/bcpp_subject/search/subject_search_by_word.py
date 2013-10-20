from edc.dashboard.search.classes import BaseSearchByWord

from ..models import SubjectConsent


class SubjectSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = SubjectConsent
    order_by = '-created'
    template = 'subjectconsent_include.html'

    def contribute_to_context(self, context):
        context = super(BaseSearchByWord, self).contribute_to_context(context)
        # FIXME: this should not be hard coded, get it from the section class somehow.
        context.update({
            'subject_dashboard_url': 'subject_dashboard_url'})
        return context
