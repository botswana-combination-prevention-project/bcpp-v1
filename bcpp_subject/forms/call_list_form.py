from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import CallList


class CallListForm (BaseModelForm):

    class Meta:
        model = CallList
