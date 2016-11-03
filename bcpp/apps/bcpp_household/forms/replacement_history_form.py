from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import ReplacementHistory


class ReplacementHistoryForm(BaseModelForm):

    class Meta:
        model = ReplacementHistory
