from edc.base.form.forms import BaseModelForm

from ..models import HouseholdWorkList


class HouseholdWorkListForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = HouseholdWorkList
