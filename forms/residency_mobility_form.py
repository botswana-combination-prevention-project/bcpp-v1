from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import ResidencyMobility


#ResidencyMobility
class ResidencyMobilityForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #validating if other community, you specify
        if cleaned_data.get('cattle_postlands') == 'Other community' and not cleaned_data.get('cattle_postlands_other'):
            raise forms.ValidationError('If participant was staying in another community, specify the community')
#         #if reason for staying away is OTHER, specify reason
#         if cleaned_data.get('reason_away') == 'Other' and not cleaned_data.get('reason_away_other'):
#             raise forms.ValidationError('If participant was away from community for \'OTHER\' reason, provide/specify reason')
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        return cleaned_data

    class Meta:
        model = ResidencyMobility
