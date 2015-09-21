from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..models import SubjectHtcHistory


class SubjectHtcHistoryAdmin(BaseRegisteredSubjectModelAdmin):

    fields = (
        'household_member',
        'report_datetime',
        'offered',
        'accepted',
        'refusal_reason',
        'tracking_identifier',
        'referred',
        'referral_clinic')

    radio_fields = {"offered": admin.VERTICAL,
                    "accepted": admin.VERTICAL,
                    "referred": admin.VERTICAL}

    list_display = ('household_member', 'report_datetime', 'tracking_identifier')

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier',
        'tracking_identifier']

    list_filter = ('household_member__household_structure__household__community', 'report_datetime', 'offered', 'accepted', 'referred', 'referral_clinic')

    instructions = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectHtcHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectHtcHistory, SubjectHtcHistoryAdmin)
