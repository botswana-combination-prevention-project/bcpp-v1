from django import forms


class BaseVisitTrackingForm(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('appointment', None):
            appointment = cleaned_data.get('appointment')
            dispatched, producer_name = appointment.registered_subject.is_dispatched_to_producer()
            if dispatched:
                raise forms.ValidationError("Data for {0} is currently dispatched to netbook {1}. "
                                 "This form may not be modified.".format(appointment.registered_subject.subject_identifier,
                                                                          producer_name))
        return cleaned_data
