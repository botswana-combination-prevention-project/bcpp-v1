from django.contrib import admin
from bhp_consent.admin import BaseConsentModelAdmin
from bhp_registration.models import RegisteredSubject
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.forms import SubjectConsentYearOneForm, SubjectConsentYearTwoForm, SubjectConsentYearThreeForm, SubjectConsentYearFourForm, SubjectConsentYearFiveForm
from bcpp_subject.models import SubjectConsentYearOne, SubjectConsentYearTwo, SubjectConsentYearThree, SubjectConsentYearFour, SubjectConsentYearFive


class BaseSubjectConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'subject'

    def __init__(self, *args, **kwargs):
        super(BaseSubjectConsentAdmin, self).__init__(*args, **kwargs)
        for i, item in enumerate(self.fields):
            if item == 'assessment_score':
                del self.fields[i]
        self.fields.insert(0, 'registered_subject')
        self.fields.insert(0, 'household_structure_member')
        self.search_fields.append('household_structure_member__household_structure__household__household_identifier')
        self.radio_fields.update({"is_minor": admin.VERTICAL})

    def save_model(self, request, obj, form, change):
        super(BaseSubjectConsentAdmin, self).save_model(request, obj, form, change)
        # update hsm member_status
        household_structure_member = obj.household_structure_member
        household_structure_member.member_status = 'CONSENTED'
        household_structure_member.save()

    def delete_model(self, request, obj):
        # update hsm member_status
        household_structure_member = obj.household_structure_member
        household_structure_member.member_status = None
        household_structure_member.save()
        return super(BaseSubjectConsentAdmin, self).delete_model(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure_member":
            kwargs["queryset"] = HouseholdStructureMember.objects.filter(id__exact=request.GET.get('household_structure_member', 0))
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
        return super(BaseSubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SubjectConsentYearOneAdmin(BaseSubjectConsentAdmin):
    form = SubjectConsentYearOneForm
admin.site.register(SubjectConsentYearOne, SubjectConsentYearOneAdmin)


class SubjectConsentYearTwoAdmin(BaseSubjectConsentAdmin):

    form = SubjectConsentYearTwoForm

    def __init__(self, *args, **kwargs):
        super(SubjectConsentYearTwoAdmin, self).__init__(*args, **kwargs)
        # add 'is_minor' before guardian name
        for i, fld in enumerate(self.fields):
            if fld == 'guardian_name':
                self.fields.insert(i, 'is_minor')
                break
admin.site.register(SubjectConsentYearTwo, SubjectConsentYearTwoAdmin)


class SubjectConsentYearThreeAdmin(BaseSubjectConsentAdmin):
    form = SubjectConsentYearThreeForm
admin.site.register(SubjectConsentYearThree, SubjectConsentYearThreeAdmin)


class SubjectConsentYearFourAdmin(BaseSubjectConsentAdmin):
    form = SubjectConsentYearFourForm
admin.site.register(SubjectConsentYearFour, SubjectConsentYearFourAdmin)


class SubjectConsentYearFiveAdmin(BaseSubjectConsentAdmin):
    form = SubjectConsentYearFiveForm
admin.site.register(SubjectConsentYearFive, SubjectConsentYearFiveAdmin)

# 
# # SubjectConsent
# class SubjectConsentAdmin(BaseConsentModelAdmin):
#     date_heirarchy = 'consent_datetime'
#     form = SubjectConsentForm
#     fields = (
#         "subject_identifier",
# #         "registered_subject",
#         "first_name",
#         "last_name",
#         "initials",
#         "consent_datetime",
#         "gender",
#         "study_site",
#         "guardian_name",
#         "dob",
#         "is_dob_estimated",
#         "identity",
#         "identity_type",
#         "confirm_identity",
#         "may_store_samples",
#         "is_incarcerated",
#         "is_literate",
#         "witness_name",
#         "comment",
#         "consent_reviewed",
#         "study_questions",
#         "assessment_score",
#         "consent_copy")
#     radio_fields = {
#         "study_site": admin.VERTICAL,
#         "identity_type": admin.VERTICAL,
#         "may_store_samples": admin.VERTICAL,
#         "gender": admin.VERTICAL,
#         "is_dob_estimated": admin.VERTICAL,
#         "is_incarcerated": admin.VERTICAL, 
#         "is_literate": admin.VERTICAL,
#         "consent_reviewed": admin.VERTICAL,
#         "study_questions": admin.VERTICAL,
#         "assessment_score": admin.VERTICAL,
#         "consent_copy": admin.VERTICAL}
#     readonly_fields = ('subject_identifier',)
# 
# admin.site.register(SubjectConsent, SubjectConsentAdmin)
