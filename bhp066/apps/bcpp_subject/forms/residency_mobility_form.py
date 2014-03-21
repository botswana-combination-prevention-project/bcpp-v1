from django import forms
from ..models import ResidencyMobility
from .base_subject_model_form import BaseSubjectModelForm


# ResidencyMobility
class ResidencyMobilityForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = ResidencyMobility(**self.cleaned_data)
        # validating that residency status is not changed after capturing enrollment checklist
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating if other community, you specify
        if cleaned_data.get('cattle_postlands') == 'Other community' and not cleaned_data.get('cattle_postlands_other'):
            raise forms.ValidationError('If participant was staying in another community, specify the community')

        # this as in redmine issue 69
        if cleaned_data.get('nights_away') == 'zero' and cleaned_data.get('cattle_postlands') != 'N/A':
            raise forms.ValidationError('If participant spent zero nights away, times spent away should be Not applicable')

        if cleaned_data.get('nights_away') != 'zero' and cleaned_data.get('cattle_postlands') == 'N/A':
            raise forms.ValidationError('Participant has spent more than zero nights away, times spent away CANNOT be Not applicable')

        return cleaned_data

    class Meta:
        model = ResidencyMobility
