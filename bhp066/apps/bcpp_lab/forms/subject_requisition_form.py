from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import SubjectRequisition


class SubjectRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(SubjectRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    class Meta:
        model = SubjectRequisition
