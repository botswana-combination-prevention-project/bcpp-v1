from django import forms
from bhp_dispatch.helpers import is_dispatched_registered_subject
from bhp_consent.forms import BaseConsentedModelForm


class BaseVisitTrackingForm(BaseConsentedModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('appointment', None):
            appointment = cleaned_data.get('appointment')
            dispatched, producer_name = is_dispatched_registered_subject(appointment.registered_subject)
            if dispatched:
                raise forms.ValidationError("Data for {0} is currently dispatched to netbook {1}. "
                                 "This form may not be modified.".format(appointment.registered_subject.subject_identifier,
                                                                          producer_name))
        return cleaned_data
