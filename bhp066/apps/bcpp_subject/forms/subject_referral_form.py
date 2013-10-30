from ..models import SubjectReferral
from .base_subject_model_form import BaseSubjectModelForm


class SubjectReferralForm(BaseSubjectModelForm):

#     def clean(self):
#         cleaned_data = super(SubjectReferralForm, self).clean()
#
#         return cleaned_data

    class Meta:
        model = SubjectReferral
