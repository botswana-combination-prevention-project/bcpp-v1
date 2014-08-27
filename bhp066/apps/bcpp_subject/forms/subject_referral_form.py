from django import forms

from ..classes import SubjectReferralHelper
from ..models import SubjectReferral

from .base_subject_model_form import BaseSubjectModelForm


class SubjectReferralForm(BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(SubjectReferralForm, self).clean()
        subject_referral_helper = SubjectReferralHelper(SubjectReferral(**cleaned_data))
        if subject_referral_helper.missing_data:
            raise forms.ValidationError('Some data is missing for the referral. Complete \'{0}\' first '
                                        'and try again.'.format(subject_referral_helper.missing_data._meta.verbose_name))
#         if subject_referral_helper.referral_code and (
#                 not subject_referral_helper.referral_appt_datetime or
#                 not subject_referral_helper.referral_clinic_type):
#             raise forms.ValidationError('Need referral_code, referral_appt_date and referral_clinic_type to continue. '
#                                         'Got {0}.'.format([subject_referral_helper.referral_code,
#                                                           subject_referral_helper.referral_appt_datetime,
#                                                           subject_referral_helper.referral_clinic_type]))
        return cleaned_data

    class Meta:
        model = SubjectReferral
