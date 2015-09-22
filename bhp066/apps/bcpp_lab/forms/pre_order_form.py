from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import PreOrder


class PreOrderForm (BaseModelForm):

    class Meta:
        model = PreOrder
