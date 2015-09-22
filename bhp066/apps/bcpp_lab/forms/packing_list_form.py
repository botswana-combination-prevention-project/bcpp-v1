from edc.lab.lab_packing.forms import BasePackingListForm, BasePackingListItemForm

from ..models import SubjectRequisition, ClinicRequisition, PackingList, PackingListItem, Aliquot


class PackingListForm (BasePackingListForm):

    def clean(self):
        self.requisition = [SubjectRequisition, ClinicRequisition, Aliquot]
        return super(PackingListForm, self).clean()

    class Meta:
        model = PackingList


class PackingListItemForm (BasePackingListItemForm):

    def clean(self):
        self.requisition = [SubjectRequisition, ClinicRequisition, Aliquot]
        return super(BasePackingListItemForm, self).clean()

    class Meta:
        model = PackingListItem
