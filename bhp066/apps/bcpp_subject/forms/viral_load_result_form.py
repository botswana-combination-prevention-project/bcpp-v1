from edc.base.form.forms import BaseModelForm
from ..models import ViralLoadResult


class ViralLoadResultForm (BaseModelForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = ViralLoadResult
