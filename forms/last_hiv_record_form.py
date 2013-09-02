from django import forms
from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import LastHivRecord


class LastHivRecordForm (BaseHtcModelForm):

    def clean(self):
        cleaned_data = super(LastHivRecordForm, self).clean()
        # validating HIV care
        if cleaned_data.get('attended_hiv_care') == 'Yes' and not cleaned_data.get('hiv_care_clinic'):
            raise forms.ValidationError('If participant has attended an HIV care clinic,'
                                        ' what is the name of that clinic?')
        return cleaned_data

    class Meta:
        model = LastHivRecord
