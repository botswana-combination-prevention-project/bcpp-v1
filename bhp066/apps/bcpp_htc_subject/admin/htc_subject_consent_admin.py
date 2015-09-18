from django.contrib import admin

from edc.subject.consent.admin import BaseConsentModelAdmin
from edc.subject.registration.models import RegisteredSubject

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..models import HtcSubjectConsent

from ..forms import HtcSubjectConsentForm


class HtcSubjectConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'htc_subject'
    form = HtcSubjectConsentForm

    def __init__(self, *args, **kwargs):
        super(HtcSubjectConsentAdmin, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'household_member')
        self.search_fields.append('household_member__household_structure__household__household_identifier')
        self.radio_fields.update({"is_minor": admin.VERTICAL})

    def save_model(self, request, obj, form, change):
        super(HtcSubjectConsentAdmin, self).save_model(request, obj, form, change)
        # update hm member_status
        household_member = obj.household_member
        household_member.member_status = 'CONSENTED'
        household_member.save()

    def delete_model(self, request, obj):
        # update hm member_status
        household_member = obj.household_member
        household_member.member_status = None
        household_member.save()
        return super(HtcSubjectConsentAdmin, self).delete_model(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
        return super(HtcSubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HtcSubjectConsent, HtcSubjectConsentAdmin)
