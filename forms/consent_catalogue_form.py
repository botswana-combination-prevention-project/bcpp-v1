from bhp_base_form.forms import BaseModelForm


class ConsentCatalogueForm (BaseModelForm):

    def clean(self, consent_instance=None):
        cleaned_data = self.cleaned_data

#        name = cleaned_data.get('name', None)
#        version = cleaned_data.get('version', None)
#        start_datetime = cleaned_data.get('start_datetime', None)
#        end_datetime = cleaned_data.get('end_datetime', None)
#        if name and version:
#            consent_catalogue = self._meta.model.objects.filter(name=name).order_by('version')
#            # ensure start_datetime of next version does not

        return cleaned_data
