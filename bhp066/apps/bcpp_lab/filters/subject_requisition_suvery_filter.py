from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..models import SubjectRequisition

survey_slugs = (
    ('bcpp-year-1', 'bcpp-year-1'),
    ('bcpp-year-2', 'bcpp-year-2'),
    ('bcpp-year-3', 'bcpp-year-3'),
)


class SubjectRequisitionSurveyFilter(SimpleListFilter):

    title = _('survey')
    parameter_name = 'survey'

    def lookups(self, request, model_admin):
        return survey_slugs

    def queryset(self, request, queryset):
        if self.value():
            requisition = SubjectRequisition.objects.filter(subject_visit__household_member__household_structure__survey__survey_slug=self.value())
            req_ids = [req.id for req in requisition]
            return queryset.filter(id__in=req_ids)
        return queryset
