from edc.base.form.forms import BaseModelForm

from ..models import HouseholdEnumerationRefusal


class HouseholdEnumerationRefusalForm(BaseModelForm):

    class Meta:
        model = HouseholdEnumerationRefusal
