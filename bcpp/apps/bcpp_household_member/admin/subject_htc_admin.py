from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..models import SubjectHtc

from ..forms import SubjectHtcForm


class SubjectHtcAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectHtcForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'household_member',
        'report_datetime',
        'tracking_identifier',
        'offered',
        'accepted',
        'refusal_reason',
        'referred',
        'referral_clinic',
        'comment')

    radio_fields = {
        "offered": admin.VERTICAL,
        "accepted": admin.VERTICAL,
        "referred": admin.VERTICAL,
    }

    list_display = ('household_member', 'tracking_identifier', 'report_datetime', 'offered', 'accepted', 'referred')

    search_fields = [
        'tracking_identifier',
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('report_datetime', 'offered', 'accepted', 'referred',
                   'household_member__household_structure__household__community')

    def get_readonly_fields(self, request, obj=None):
        super(SubjectHtcAdmin, self).get_readonly_fields(request, obj)
        return ('tracking_identifier',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectHtcAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectHtc, SubjectHtcAdmin)
