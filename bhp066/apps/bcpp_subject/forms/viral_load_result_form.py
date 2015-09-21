from bhp066.apps.bcpp.base_model_form import BaseModelForm
from ..models import ViralLoadResult


class ViralLoadResultForm (BaseModelForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = ViralLoadResult
