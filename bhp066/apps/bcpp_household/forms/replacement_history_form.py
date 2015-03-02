from edc.base.form.forms import BaseModelForm

from ..models import ReplacementHistory


class ReplacementHistoryForm(BaseModelForm):

    class Meta:
        model = ReplacementHistory
