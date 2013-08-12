from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import CommunityEngagement



class CommunityEngagementForm (BaseSubjectModelForm):
    
    def clean(self):
 
        cleaned_data = self.cleaned_data
        # validating other
        if cleaned_data.get('problems_engagement')[0].name == 'Other, specify' and not cleaned_data.get('problems_engagement_other'):
            raise forms.ValidationError('If there are other problems, please indicate.')
 
        cleaned_data = super(CommunityEngagementForm, self).clean()
 
        return cleaned_data


    class Meta:
        model = CommunityEngagement
