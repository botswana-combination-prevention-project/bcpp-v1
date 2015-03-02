from django import forms

from ..models import HeartAttack, Cancer, Tubercolosis, Sti

from .base_subject_model_form import BaseSubjectModelForm


class HeartAttackForm (BaseSubjectModelForm):

    class Meta:
        model = HeartAttack


class CancerForm (BaseSubjectModelForm):

    class Meta:
        model = Cancer


class TubercolosisForm (BaseSubjectModelForm):

    class Meta:
        model = Tubercolosis


class StiForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(StiForm, self).clean()
        # to ensure that STI diagnosis date is not greater than today
#         if cleaned_data.get('sti_date'):
#             if cleaned_data.get('sti_date') > date.today():
#                 raise forms.ValidationError('The STI diagnoses date date cannot be greater than today\'s date. Please correct.')
        # It None in diagnosis, then ensure no date is entered.
        if ((cleaned_data.get('sti_dx') is None or cleaned_data.get('sti_dx')[0].name == 'None') and ((cleaned_data.get('wasting_date') is not None) or
            (cleaned_data.get('yeast_infection_date') is not None) or (cleaned_data.get('pneumonia_date') is not None) or (cleaned_data.get('pcp_date') is not None) or
                (cleaned_data.get('herpes_date') is not None) or (cleaned_data.get('diarrhoea_date') is not None))):
            raise forms.ValidationError('If participant has never had any illness, then do not provide any dates.')
        # wasting
        if cleaned_data.get('sti_dx')[0].name == 'Severe weight loss (wasting) - more than 10% of body weight' and not cleaned_data.get('wasting_date'):
            raise forms.ValidationError('If participant has ever been diagnosed with wasting, what is the date of diagnosis?')
        # diarrhoea
        if cleaned_data.get('sti_dx')[0].name == 'Unexplained diarrhoea for one month' and not cleaned_data.get('diarrhoea_date'):
            raise forms.ValidationError('If participant has ever been diagnosed with diarrhoea, what is the diagnosis date?')
        # yesat_infection
        if cleaned_data.get('sti_dx')[0].name == 'Yeast infection of mouth or oesophagus' and not cleaned_data.get('yeast_infection_date'):
            raise forms.ValidationError('If participant has ever been diagnosed with yeast infection, what is the diagnosis date?')
        # pneumonia
        if cleaned_data.get('sti_dx')[0].name == 'Severe pneumonia or meningitis or sepsis' and not cleaned_data.get('pneumonia_date'):
            raise forms.ValidationError('If participant has ever been diagnosed with pneumonia_date, what is the date of diagnosis?')
        # pcp
        if cleaned_data.get('sti_dx')[0].name == 'PCP (Pneumocystis pneumonia)' and not cleaned_data.get('pcp_date'):
            raise forms.ValidationError('If participant has ever been diagnosed with PCP, what is the date of diagnosis?')
        # herpes
        if cleaned_data.get('sti_dx')[0].name == 'Herpes infection for more than one month' and not cleaned_data.get('herpes_date'):
            raise forms.ValidationError('If participant has ever been diagnosed with Herpes for more than a month, what is the date of diagnosis?')
        return cleaned_data

    class Meta:
        model = Sti
