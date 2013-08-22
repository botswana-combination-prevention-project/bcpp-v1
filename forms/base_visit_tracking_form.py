from django import forms
from django.conf import settings
from bhp_consent.forms import BaseConsentedModelForm


class BaseVisitTrackingForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseVisitTrackingForm, self).__init__(*args, **kwargs)
        self._validation_error = None

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
        self._validate_cleaned_data(cleaned_data)
        return cleaned_data

    def set_validation_error(self, value=None):
        if value:
            if not isinstance(value, dict):
                raise TypeError('parameter value must be a dictionary.')
        self._validation_error = value

    def get_validation_error(self):
        if not self._validation_error:
            self.set_validation_error()
        return self._validation_error

    def _validate_cleaned_data(self, cleaned_data, supress_exception=None):

        self.validate_cleaned_data(cleaned_data)
        if self.get_validation_error() and not supress_exception:
            for message in self.get_validation_error().itervalues():
                raise forms.ValidationError(message)
        return self.get_validation_error()

    def validate_cleaned_data(self, cleaned_data, suppress_exception=None):
        """Override to add validation code in a manner that is easier to test.

        Instead of adding validation code to the clean() method, add it
        to this method. Then in your tests do something like this::
            ...
            print 'test maternal visit'
            form = MaternalVisitForm()
            self.assertEquals(form._validate_cleaned_data({}), None)
            self.assertRaises(ValidationError, form._validate_cleaned_data, {'reason': 'missed', 'reason_missed': None})
            self.assertIsNotNone(form._validate_cleaned_data({'reason': 'missed', 'reason_missed': None}, supress_exception=True).get(1, None))
            ...

        .. note:: in your test call :fun:`_validate_cleaned_data` instead of :fun:`validate_cleaned_data`

        Since :func:`clean` is called in super, there is no need to override it nor for this method
        to return cleaned_data. So instead of this, in the clean method::

            if cleaned_data.get('reason') == 'missed' and not cleaned_data.get('reason_missed'):
                raise forms.ValidationError('Please provide the reason the scheduled visit was missed')

        ... do this in :func:`validate_cleaned_data`::

            if cleaned_data.get('reason') == 'missed' and not cleaned_data.get('reason_missed'):
                self.set_validation_error({1: 'an error has occurred'})

        ... then in the test, inspect the return value::

            self.assertIsNotNone(form._validate_cleaned_data({'reason': 'missed', 'reason_missed': None}, supress_exception=True).get(1, None))

        """
        pass
