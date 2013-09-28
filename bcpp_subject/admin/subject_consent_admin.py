from django.contrib import admin
from edc_lib.bhp_consent.admin import BaseConsentModelAdmin
from edc_lib.bhp_registration.models import RegisteredSubject
from bcpp_household_member.models import HouseholdMember
from bcpp_subject.models import SubjectConsent  # YearOneForm, SubjectConsentYearTwoForm, SubjectConsentYearThreeForm, SubjectConsentYearFourForm, SubjectConsentYearFiveForm
from bcpp_subject.forms import SubjectConsentForm  # YearOne, SubjectConsentYearTwo, SubjectConsentYearThree, SubjectConsentYearFour, SubjectConsentYearFive


class SubjectConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'subject'
    form = SubjectConsentForm

    def __init__(self, *args, **kwargs):
        super(SubjectConsentAdmin, self).__init__(*args, **kwargs)
        for i, item in enumerate(self.fields):
            if item == 'assessment_score':
                del self.fields[i]
        self.fields.insert(0, 'household_member')
        self.search_fields.append('household_member__household_structure__household__household_identifier')
        self.search_fields.append('household_member__household_structure__plot__plot_identifier')
        self.radio_fields.update({"is_minor": admin.VERTICAL})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
        return super(SubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectConsent, SubjectConsentAdmin)
