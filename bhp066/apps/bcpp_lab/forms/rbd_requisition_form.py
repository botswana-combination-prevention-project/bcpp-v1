from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import RBDRequisition


class RBDRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):

        super(RBDRequisitionForm, self).__init__(*args, **kwargs)

        self.fields['item_type'].initial = 'tube'

    def clean(self):
        super(RBDRequisitionForm, self).clean()

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = RBDRequisition
