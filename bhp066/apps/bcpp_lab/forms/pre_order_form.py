from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import PreOrder


class PreOrderForm (BaseModelForm):

    def clean(self):

        return super(PreOrderForm, self).clean()

    class Meta:
        model = PreOrder
