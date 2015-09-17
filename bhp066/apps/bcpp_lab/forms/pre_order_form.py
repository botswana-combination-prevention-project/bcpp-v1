from edc.base.form.forms import BaseModelForm

from ..models import PreOrder


class PreOrderForm (BaseModelForm):

    def clean(self):

        return super(PreOrderForm, self).clean()

    class Meta:
        model = PreOrder
