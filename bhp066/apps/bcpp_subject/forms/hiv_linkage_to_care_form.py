from ..models import HivLinkageToCare
from .base_subject_model_form import BaseSubjectModelForm
from bhp066.apps.bcpp_subject.models.hiv_care_adherence import HivCareAdherence
from django import forms


class HivLinkageToCareForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(HivLinkageToCareForm, self).clean()
        instance = None
        subject_visit = None
        if self.instance.id:
            instance = self.instance
            subject_visit = self.instance.subject_visit
        else:
            instance = HivLinkageToCare(**self.cleaned_data)
            subject_visit = instance.subject_visit
        try:
            HivCareAdherence.objects.get(subject_visit=subject_visit)
        except HivCareAdherence.DoesNotExist:
            raise forms.ValidationError('Hiv Care Adherence has to be filled before filling this form.')
        return cleaned_data

    class Meta:
        model = HivLinkageToCare
