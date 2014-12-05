from edc.base.form.forms import BaseModelForm

from ..models import CallList


class CallListForm (BaseModelForm):

    class Meta:
        model = CallList
