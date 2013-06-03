from django import forms
from django.conf import settings
from django.db.models import OneToOneField, ForeignKey, get_model
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_base_form.classes import LogicCheck


class BaseModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        self.logic = LogicCheck(self._meta.model)
        # if in admin edit mode, populate visit model's queryset
        # if not in admin, e.g. coming from the dashboard, might
        # throw an exception.
        if self.instance:
            if 'get_visit' in dir(self.instance):
                try:
                    # but if self.instance.maternal_visit DoesNotExist, will throw an exception
                    # when get_visit() is called
                    if self.instance.get_visit():
                        try:
                            attr = self.instance.get_visit()._meta.object_name.lower()
                            self.fields[attr].queryset = self.instance.get_visit().__class__.objects.filter(pk=self.instance.get_visit().pk)
                        except KeyError:
                            pass
                except:
                    pass
        # if in admin edit mode, populate registered_subject's queryset

        if 'registered_subject' in self.fields:
            try:
                if 'registered_subject' in dir(self.instance):
                        if self.instance.registered_subject:
                            self.fields['registered_subject'].queryset = self.instance.registered_subject.__class__.objects.filter(pk=self.instance.registered_subject.pk)
                else:
                    self.fields['registered_subject'].queryset = self.instance.registered_subject.__class__.objects.none()
            except:
                if 'registered_subject' not in self.initial and 'registered_subject' not in self.data:
                    RegisteredSubject = get_model('bhp_registration', 'RegisteredSubject')
                    self.fields['registered_subject'].queryset = RegisteredSubject.objects.none()
        # translation
        self.insert_translation_attributes()

    def insert_translation_attributes(self):
        for k in self.fields.iterkeys():
            self.fields[k].widget.attrs['translation'] = 'This test needs a translation'
        return None

    def get_subject_identifier(self, cleaned_data):
        subject_identifier = None
        if 'subject_identifier' in cleaned_data:
            subject_identifier = cleaned_data.get('subject_identifier')
        if not subject_identifier:
            if 'registered_subject' in cleaned_data:
                subject_identifier = cleaned_data.get('registered_subject').subject_identifier
        if not subject_identifier:
            # look for a visit model field
            for field in self._meta.model._meta.fields:
                if isinstance(field, (OneToOneField, ForeignKey)):
                    if isinstance(field.rel.to, BaseVisitTracking):
                        attrname = field.attrname
                        visit = cleaned_data.get(attrname, None)
                        if visit:
                            subject_identifier = visit.get_subject_identifier()
        return subject_identifier

    def clean(self):

        cleaned_data = self.cleaned_data
        # check if dispatched
        if 'bhp_dispatch' in settings.INSTALLED_APPS:
            if 'is_dispatched' in dir(self._meta.model()):
                if self._meta.model().is_dispatched:
                    raise forms.ValidationError('Cannot update. Form is currently dispatched')
        # encrypted fields may have their own validation code to run.
        # See the custom field objects in bhp_crypto.
        try:
            from bhp_crypto.classes import BaseEncryptedField
            for field in self._meta.model._meta.fields:
                if isinstance(field, BaseEncryptedField):
                    field.validate_with_cleaned_data(field.attname, cleaned_data)
        except ImportError:
            pass
        other = []
        [other.append(k) for k in cleaned_data.iterkeys() if cleaned_data[k] == 'OTHER']
        for k in other:
            if '{0}_other'.format(k) in cleaned_data:
                if not cleaned_data['{0}_other'.format(k)]:
                    raise forms.ValidationError('If {0} is \'OTHER\', please specify. '
                                                'You wrote \'{1}\''.format(k, cleaned_data['{0}_other'.format(k)]))
        return super(BaseModelForm, self).clean()

    def validate_m2m(self, **kwargs):

        """Validates at form level a triplet of questions lead by a Yes/No for a many to many with other specify.

            * The first question is a Yes/No question indicating if any items in the many to many will be selected
            * The second question is a many to many (select all that apply)
            * The third is an 'Other Specify' to be completed if an 'Other' item was selected in the many to many question

            Be sure to check cleaned_data for the 'key' of the m2m field first.

            For example, in the ModelForm clean() method call::

                if cleaned_data.has_key('chronic_cond'):
                    self.validate_m2m(
                            label = 'chronic condition',
                            yesno = cleaned_data['has_chronic_cond'],
                            m2m = cleaned_data['chronic_cond'],
                            other = cleaned_data['chronic_cond_other'])
        """

        label = kwargs.get('label', 'items to be selected')
        leading = kwargs.get('leading')
        m2m = kwargs.get('m2m')
        other = kwargs.get('other')

        # if leading question is 'Yes', a m2m item cannot be 'Not applicable'
        if leading.lower() == 'yes' and [True for item in m2m if item.name.lower() == 'not applicable']:
            raise forms.ValidationError("You stated there ARE " + label + "s, yet you selected '{0}'".format(item.name))

        # if leading question is 'No', ensure the m2m item is 'not applicable'
        if leading.lower() == 'no' and not [True for item in m2m if item.name.lower() == 'not applicable']:
            raise forms.ValidationError("You stated there are NO {0}s. Please correct".format(label))

        # if leading question is 'No', ensure only one m2m item is selected.
        if leading.lower() == 'no' and len(m2m) > 1:
            raise forms.ValidationError("You stated there are NO {0}s. Please correct".format(label))

        # if leading question is 'Yes' and an m2m item is 'other, specify', ensure 'other' attribute has a value
        if leading.lower() == 'yes' and not other and [True for item in m2m if 'other' in item.name.lower()]:
            raise forms.ValidationError("You have selected a '{0}' as 'Other', please specify.".format(label))

        # if 'other' has a value but no m2m item is 'Other, specify'
        if other and not [True for item in m2m if 'other' in item.name.lower()]:
            raise forms.ValidationError("You have specified an 'Other' {0} but not selected 'Other, specify'. Please correct.".format(label))
