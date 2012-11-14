from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django import forms
from bhp_variables.models import StudySpecific
from bhp_variables.choices import GENDER_OF_CONSENT
from bhp_common.utils import formatted_age
from bhp_base_form.classes import BaseModelForm


class BaseSubjectConsentForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        """
        check omang if identity_type is omang
        """
        # encrypted fields may cause problems if existing values
        # cannot be decrypted, so call a custom field method validate_with_cleaned_data()
        # to validate.
        #for field in self._meta.model._meta.fields:
        #    if isinstance(field, BaseEncryptedField):
        #        field.validate_with_cleaned_data(field.attname, cleaned_data)

        """
        check 1st and last letters of initials match subjects name
        """
        #        my_first_name = cleaned_data.get("first_name")
        #        my_last_name = cleaned_data.get("last_name")
        #        my_initials = cleaned_data.get("initials"
        #        check_initials_field(my_first_name, my_last_name, my_initials)

        """
        if minor, force specify guardian's name
        """
        try:
            obj = StudySpecific.objects.all()[0]
        except IndexError:
            raise TypeError("Please add your bhp_variables site specifics")

        if cleaned_data.get('dob'):
            rdelta = relativedelta(date.today(), cleaned_data.get('dob'))
            # check if guardian name is required
            # guardian name is required if subject is a minor but the field may not be on the form
            # if the study does not have minors.
            if rdelta.years < obj.age_at_adult_lower_bound:
                if "guardian_name" not in cleaned_data.keys():
                    raise forms.ValidationError('Subject is a minor. "guardian_name" is required but missing from the form. Please add this field to the form.')
                elif "guardian_name" in cleaned_data.keys() and cleaned_data.get("guardian_name", None) == '':
                    raise forms.ValidationError(u'Subject\'s age is %s. Subject is a minor. Guardian\'s name is required.' % (formatted_age(cleaned_data.get('dob'), date.today())))
                else:
                    pass
            if rdelta.years >= obj.age_at_adult_lower_bound and "guardian_name" in cleaned_data.keys():
                if not cleaned_data.get("guardian_name", None) == '':
                    raise forms.ValidationError(u'Subject\'s age is %s. Subject is an adult. Guardian\'s name is NOT required.' % (formatted_age(cleaned_data.get('dob'), date.today())))
        # if consent model has a ConsentAge method that returns an ordered range of ages as list
        if hasattr(self._meta.model, 'ConsentAge'):
            instance = self._meta.model()
            consent_age_range = instance.ConsentAge()
            rdelta = relativedelta(datetime.today(), cleaned_data.get('dob'))
            if rdelta.years not in consent_age_range:
                raise forms.ValidationError("Invalid Date of Birth. Age of consent must be between %sy and %sy inclusive. Got %sy" % (consent_age_range[0], consent_age_range[-1], rdelta.years,))

        # check for gender of consent
        if cleaned_data.get('gender'):
            study_specific = StudySpecific.objects.all()[0]
            gender_of_consent = study_specific.gender_of_consent
            if gender_of_consent == 'MF':
                allowed = ('MF', 'Male and Female')
                entry = ('value', cleaned_data.get('gender'))
            else:
                for lst in GENDER_OF_CONSENT:
                    if lst[0] == gender_of_consent:
                        allowed = lst
                for lst in GENDER_OF_CONSENT:
                    if lst[0] == cleaned_data.get('gender'):
                        entry = lst
            if cleaned_data.get('gender') != allowed[0] and allowed[0] != 'MF':
                raise forms.ValidationError(u'Gender of consent is %s. You entered %s.' % (allowed[1], entry[1]))
        # confirm attr identity and confirm_identity match
        if cleaned_data.get('identity') and cleaned_data.get('confirm_identity'):
            if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
                raise forms.ValidationError('Identity mismatch. Identity number must match the confirmation field.')
        # Always return the full collection of cleaned data.
        return cleaned_data
