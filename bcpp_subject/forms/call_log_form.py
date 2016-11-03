from django import forms

from bhp066.apps.bcpp.base_model_form import BaseModelForm
from edc_constants.constants import ALIVE, DEAD, NO, YES, UNKNOWN

from ..models import CallLog, CallLogEntry


class CallLogForm (BaseModelForm):

    class Meta:
        model = CallLog


class CallLogEntryForm (BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        self.survival_status()

        if cleaned_data.get('appt') == NO and cleaned_data.get('appt_date'):
            raise forms.ValidationError('You may not schedule an appointment for a participant who is not willing '
                                        'to schedule an appointment.')

        if cleaned_data.get('appt') == YES and not cleaned_data.get('appt_date'):
            raise forms.ValidationError('Subject is willing to schedule an appointment. '
                                        'Please indicate the appointment date.')

        if cleaned_data.get('available') == NO and cleaned_data.get('appt_date'):
            raise forms.ValidationError('You may not schedule an appointment for a participant who is not available '
                                        'during the survey.')

        if cleaned_data.get('contact_type') != 'direct' and cleaned_data.get('appt_date'):
            raise forms.ValidationError('You may may only schedule an appointment if contact is '
                                        'with the participant. Got contact_type=\'{}\''.format(
                                            cleaned_data.get('contact_type')))

        if cleaned_data.get('survival_status') == DEAD:
            for item, value in cleaned_data.iteritems():
                if value and item not in ['id', 'survival_status',
                                          'call_log', 'call_datetime', 'contact_type', 'invalid_numbers', 'call_again']:
                    raise forms.ValidationError(
                        '{} should be left blank. Got \'{}\' when survival status=Dead'.format(item, value))
            if cleaned_data.get('call_again') != NO:
                raise forms.ValidationError('Indicate NOT to call participant again. Got survival_status=\'Dead\'')

        self.contact_type_no_contact()

        if cleaned_data.get('moved_community') == YES and not cleaned_data.get('new_community'):
            raise forms.ValidationError('Specify the name of the new community or UNKNOWN. Got participant has '
                                        'moved out of the community.')

        self.moved_community_yes()

        return self.cleaned_data

    def survival_status(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('survival_status') == DEAD and cleaned_data.get('appt_date'):
            raise forms.ValidationError('You may not schedule an appointment for a participant who is deceased. '
                                        'Got survival status = Dead.')

        if cleaned_data.get('survival_status') == DEAD and cleaned_data.get('appt') == YES:
            raise forms.ValidationError('Subject is willing to schedule an appointment but got '
                                        'survival status = Dead. Please correct.')

        if cleaned_data.get('survival_status') != ALIVE and cleaned_data.get('contact_type') == 'direct':
            raise forms.ValidationError('You indicate direct contact with the participant but '
                                        'survival status suggests otherwise. Got survival_status={}'.format(
                                            cleaned_data.get('survival_status')))

    def contact_type_no_contact(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('contact_type') == 'no_contact':
            for item, value in cleaned_data.iteritems():
                if value and item not in ['id', 'call_log', 'call_datetime', 'contact_type', 'survival_status',
                                          'invalid_numbers', 'call_again']:
                    raise forms.ValidationError(
                        '{} should be left blank. Got \'{}\' when contact_type=\'No contact made\''.format(item, value))
            if cleaned_data.get('call_again') != YES and cleaned_data.get('survival_status') != DEAD:
                raise forms.ValidationError('Indicate to call participant again. Got contact_type=\'No contact made\'')
            if cleaned_data.get('survival_status') != UNKNOWN:
                raise forms.ValidationError(
                    'Expected survival status to be unknown. Got contact_type=\'No contact made\'')

    def moved_community_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('moved_community') == YES:
            for item, value in cleaned_data.iteritems():
                if value and item not in [
                        'id', 'call_log', 'call_datetime', 'contact_type', 'survival_status',
                        'invalid_numbers', 'call_again', 'new_community', 'update_locator',
                        'moved_community', 'available', 'appt', 'appt_date', 'appt_grading',
                        'time_of_week', 'time_of_day', 'appt_location', 'appt_location_other']:
                    raise forms.ValidationError(
                        'Question {} should be left blank. Got \'{}\' when moved_community=\'Yes\''.format(item, value))

    class Meta:
        model = CallLogEntry
