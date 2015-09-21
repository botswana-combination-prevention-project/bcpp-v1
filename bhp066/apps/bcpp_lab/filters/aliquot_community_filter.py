from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_subject.constants import VIRAL_LOAD, POC_VIRAL_LOAD
from bhp066.apps.bcpp.choices import YES_NO

from ..models import SubjectRequisition, Receive, PreOrder


class AliquotCommunityFilter(SimpleListFilter):

    title = _('community')
    parameter_name = 'community'

    def lookups(self, request, model_admin):
        return COMMUNITIES

    def queryset(self, request, queryset):
        if self.value():
            requisition = SubjectRequisition.objects.filter(community__icontains=self.value())
            req_identifiers = [req.requisition_identifier for req in requisition]
            receives = Receive.objects.filter(requisition_identifier__in=req_identifiers)
            return queryset.filter(receive__in=receives)
        return queryset


class PocViralLoadRequsitions(SimpleListFilter):

    title = _('poc_vl')
    parameter_name = 'poc_vl'

    def lookups(self, request, model_admin):
        return YES_NO

    def queryset(self, request, queryset):
        if self.value() and self.value() == 'Yes':
            result = queryset.filter(
                panel__name=VIRAL_LOAD,
                subject_visit__in=[pre.subject_visit for pre in PreOrder.objects.filter(panel__name=POC_VIRAL_LOAD)])
            return result
        elif self.value() and self.value() == 'No':
            result = queryset.filter(
                ~Q(panel__name=VIRAL_LOAD) & ~Q(
                    subject_visit__in=[pre.subject_visit for pre in PreOrder.objects.filter(
                        panel__name=POC_VIRAL_LOAD)])
            )
            return result
        else:
            return queryset
