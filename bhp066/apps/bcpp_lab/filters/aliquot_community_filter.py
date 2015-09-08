from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict

from apps.bcpp.choices import COMMUNITIES

from ..models import SubjectRequisition, Receive


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
