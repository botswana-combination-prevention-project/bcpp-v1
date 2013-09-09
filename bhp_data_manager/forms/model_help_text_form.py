from django import forms
from django.db.models import get_model
from bhp_base_form.forms import BaseModelForm
from bhp_data_manager.models import ModelHelpText


class ModelHelpTextForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        model = get_model(cleaned_data.get('app_label', None), cleaned_data.get('module_name', None))
        if not model:
            raise forms.ValidationError('app_label and/or module name are invalid')
#         if cleaned_data.get('field_name', None) not in [f.name for f in model._meta.fields]:
#             raise forms.ValidationError('field name {0} is invalid. Not found in {1}.'.format(cleaned_data.get('field_name', None), model._meta.fields))
        return cleaned_data

    class Meta:
        model = ModelHelpText
