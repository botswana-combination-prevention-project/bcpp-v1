from edc.base.form.forms import BaseModelForm

from ..models import DailyLog


class DailyLogForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(DailyLogForm, self).clean()

        return cleaned_data

    class Meta:
        model = DailyLog
