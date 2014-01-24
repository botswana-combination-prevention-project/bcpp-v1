from edc.lab.lab_requisition.forms import BaseRequisitionForm
from edc.lab.lab_packing.forms import BasePackingListForm, BasePackingListItemForm
from ..models import ClinicRequisition, ClinicPackingList, ClinicPackingListItem


class ClinicRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):

        super(ClinicRequisitionForm, self).__init__(*args, **kwargs)

        self.fields['item_type'].initial = 'dbs'

    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = ClinicRequisition


class PackingListForm (BasePackingListForm):

    def clean(self):

        self.requisition = [ClinicRequisition, ]

        return  super(PackingListForm, self).clean()

    class Meta:
        model = ClinicPackingList


class PackingListItemForm (BasePackingListItemForm):

    def clean(self):

        self.requisition = [ClinicRequisition, ]

        return  super(BasePackingListItemForm, self).clean()

    class Meta:
        model = ClinicPackingListItem
