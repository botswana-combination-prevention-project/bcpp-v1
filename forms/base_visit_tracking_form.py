from django import forms
from django.conf import settings
from bhp_consent.forms import BaseConsentedModelForm


class BaseVisitTrackingForm(BaseConsentedModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'bhp_dispatch' in dir(settings):
            if cleaned_data.get('appointment', None):
                appointment = cleaned_data.get('appointment')
                dispatch_item = appointment.get_dispatched_item()
                if dispatch_item:
                    forms.ValidationError("Data for {0} is currently dispatched to netbook {1}. "
                                          "This form may not be modified.".format(appointment.registered_subject.subject_identifier,
                                                                                  dispatch_item.producer.name))
        return cleaned_data
