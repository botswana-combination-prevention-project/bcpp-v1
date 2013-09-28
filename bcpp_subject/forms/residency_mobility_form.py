from django import forms
from bcpp_subject.models import ResidencyMobility
from base_subject_model_form import BaseSubjectModelForm


#ResidencyMobility
class ResidencyMobilityForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        #validating if other community, you specify
        if cleaned_data.get('cattle_postlands') == 'Other community' and not cleaned_data.get('cattle_postlands_other'):
            raise forms.ValidationError('If participant was staying in another community, specify the community')
        return cleaned_data

    class Meta:
        model = ResidencyMobility
