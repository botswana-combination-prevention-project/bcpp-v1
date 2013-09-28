from django.contrib import admin
from edc_lib.bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bcpp_household_member.models import HouseholdMember
from bcpp_subject.models import SubjectReferral
from bcpp_subject.forms import SubjectReferralForm


class SubjectReferralAdmin(BaseRegisteredSubjectModelAdmin):

    form = SubjectReferralForm

    def __init__(self, *args, **kwargs):

        super(SubjectReferralAdmin, self).__init__(*args, **kwargs)
        self.list_display.append('subject_referral_reason')
        self.list_display.append('referral_result')
        self.list_display.append('in_clinic')
        self.list_display.append('next_appt_datetime')
        self.list_filter.append('survey')
        self.list_filter.append('referral_result')
        self.list_filter.append('in_clinic')
        self.list_filter.append('subject_referral_reason')
        self.list_filter.append('next_appt_datetime')

    search_fields = ['household_member__first_name', 'household_member__household_structure__household__household_identifier', ]

    dashboard_type = 'subject'

    subject_identifier_attribute = 'registration_identifier'

    fields = (
        'registered_subject',
        'household_member',
        'report_datetime',
        'subject_referral_reason',
        'subject_referral_reason_other',
        'comment'
        )
    radio_fields = {"subject_referral_reason": admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        super(SubjectReferralAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectReferralAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectReferral, SubjectReferralAdmin)
