from django.db import models
from lab_packing.models import BasePackingListItem
from packing_list import PackingList
from subject_requisition import SubjectRequisition
from bhp_registration.models import RegisteredSubject


class PackingListItem(BasePackingListItem):

    packing_list = models.ForeignKey(PackingList, null=True)

    def drawn_datetime(self):
        retval = "n/a"
        if self.item_reference:
            requisition = SubjectRequisition.objects.get(
                                specimen_identifier=self.item_reference
                                )
            retval = requisition.drawn_datetime
        return retval

    def clinician(self):
        retval = "n/a"
        if self.item_reference:
            requisition = SubjectRequisition.objects.get(
                                specimen_identifier=self.item_reference
                                )
            retval = requisition.user_created
        return retval

    def gender(self):
        retval = "n/a"
        if self.item_reference:
            requisition = SubjectRequisition.objects.get(
                                specimen_identifier=self.item_reference
                                )
            subject_identifier = requisition.subject()
            if subject_identifier:
                registered_subject = RegisteredSubject.objects.get(
                                        subject_identifier=subject_identifier
                                    )
                retval = registered_subject.gender
        return retval

    class Meta:
        app_label = "bcpp_lab"
        verbose_name = 'Packing List Item'
