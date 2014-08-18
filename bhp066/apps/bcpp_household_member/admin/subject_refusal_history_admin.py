from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from apps.bcpp_household_member.models import HouseholdMember

from ..models import SubjectRefusalHistory


class SubjectRefusalHistoryAdmin(BaseRegisteredSubjectModelAdmin):

    fields = (
        'household_member',
        'report_datetime',
        'refusal_date',
        'reason',
        'reason_other')

    radio_fields = {"reason": admin.VERTICAL}

    list_display = ('household_member', 'report_datetime', )

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('reason', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectRefusalHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectRefusalHistory, SubjectRefusalHistoryAdmin)
