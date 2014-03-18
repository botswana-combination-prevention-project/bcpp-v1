from django import forms
from ..models import ResidencyMobility, HicEnrollment
from .base_subject_model_form import BaseSubjectModelForm


# ResidencyMobility
class ResidencyMobilityForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(ResidencyMobilityForm, self).clean()

        # validating that residency status is not changed after capturing enrollment checklist
        if HicEnrollment.objects.filter(subject_visit = cleaned_data.get('subject_visit')).exists():
            if cleaned_data.get('permanent_resident').lower() != 'yes' or cleaned_data.get('intend_residency').lower() != 'no':
                raise forms.ValidationError('An HicEnrollment form already exists for this Subject. So \'permanent_resident\' and \'intend_residency\' cannot be changed.')
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
