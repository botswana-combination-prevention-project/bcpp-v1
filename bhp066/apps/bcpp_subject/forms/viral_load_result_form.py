from bhp066.apps.bcpp.base_model_form import BaseModelForm
from ..models import ViralLoadResult


class ViralLoadResultForm (BaseModelForm):

    class Meta:
        model = ViralLoadResult
