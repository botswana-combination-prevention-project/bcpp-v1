from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO

from bhp066.apps.bcpp_subject.constants import POC_VIRAL_LOAD

from ..models import PreOrder


class PocVLRequsitionFilter(SimpleListFilter):

    title = _('poc_vl')
    parameter_name = 'poc_vl'

    def lookups(self, request, model_admin):
        return YES_NO

    def queryset(self, request, queryset):
        if self.value():
            subject_visits = [obj.subject_visit for obj in PreOrder.objects.filter(panel__name=POC_VIRAL_LOAD)]
            if self.value() == YES:
                return queryset.filter(subject_visit__in=subject_visits)
            elif self.value() == NO:
                return queryset.exclude(subject_visit__in=subject_visits)
        return queryset
