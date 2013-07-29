from django.db.models import Q, get_model
from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from bhp_consent.forms import BaseConsentedModelForm
from bcpp_subject.choices import VISIT_INFO_SOURCE, VISIT_REASON
from bcpp_subject.models import SubjectVisit, SubjectOffStudy, SubjectDeath


class SubjectVisitForm (BaseConsentedModelForm):

    """Based on model visit.

    Attributes reason and info_source override those from the base model so that
    the choices can be custom for this app.
    """

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="If 'unscheduled', information is usually reported at the next scheduled visit, but exceptions may arise",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
        )
    info_source = forms.ChoiceField(
        label='Source of information',
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
        )

    def clean(self):

        cleaned_data = self.cleaned_data
        # TODO: review logic against choices tuples
        """validate data"""
        if cleaned_data.get('reason') == 'deferred':
            raise forms.ValidationError('Reason \'deferred\' is not valid for subject visits. Please correct.')
        if cleaned_data['reason'] == 'missed' and not cleaned_data['reason_missed']:
            raise forms.ValidationError('Please provide the reason the scheduled visit was missed')
        if cleaned_data['reason'] != 'missed' and cleaned_data['reason_missed']:
            raise forms.ValidationError("Reason for visit is NOT 'missed' but you provided a reason missed. Please correct.")
        if cleaned_data['info_source'] == 'OTHER' and not cleaned_data['info_source_other']:
            raise forms.ValidationError("Source of information is 'OTHER', please provide details below your choice")

        cleaned_data = super(SubjectVisitForm, self).clean()

        AdditionalEntryBucket = get_model('bhp_entry', 'additionalentrybucket')

        """add forms to the bucket"""
        if cleaned_data['reason'] == 'lost' or cleaned_data['reason'] == 'death' or cleaned_data['reason'] == 'off study':
            """add subject offstudy form"""
            AdditionalEntryBucket.objects.add_for(
                registered_subject=cleaned_data['appointment'].registered_subject,
                model=SubjectOffStudy,
                qset=Q(registered_subject=cleaned_data['appointment'].registered_subject),
                )
        if cleaned_data['reason'] == 'death':
            """add death form"""
            AdditionalEntryBucket.objects.add_for(
                registered_subject=cleaned_data['appointment'].registered_subject,
                model=SubjectDeath,
                qset=Q(registered_subject=cleaned_data['appointment'].registered_subject),
                )
        if cleaned_data['reason'] == 'off study':
            """add subject offstudy form"""
            AdditionalEntryBucket.objects.add_for(
                registered_subject=cleaned_data['appointment'].registered_subject,
                model=SubjectOffStudy,
                qset=Q(registered_subject=cleaned_data['appointment'].registered_subject),
                )

        return cleaned_data

    class Meta:
        model = SubjectVisit
