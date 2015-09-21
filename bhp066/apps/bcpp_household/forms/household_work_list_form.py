from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import HouseholdWorkList


class HouseholdWorkListForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = HouseholdWorkList
