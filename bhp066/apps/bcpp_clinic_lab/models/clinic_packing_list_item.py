from django.db import models
from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_packing.models import BasePackingListItem
from clinic_packing_list import ClinicPackingList
from clinic_requisition import ClinicRequisition


class ClinicPackingListItem(BasePackingListItem):

    packing_list = models.ForeignKey(ClinicPackingList, null=True)

    def drawn_datetime(self):
        retval = "n/a"
        if self.item_reference:
            requisition = ClinicRequisition.objects.get(
                                specimen_identifier=self.item_reference
                                )
            retval = requisition.drawn_datetime
        return retval

    def clinician(self):
        retval = "n/a"
        if self.item_reference:
            requisition = ClinicRequisition.objects.get(
                                specimen_identifier=self.item_reference
                                )
            retval = requisition.user_created
        return retval

    def gender(self):
        retval = "n/a"
        if self.item_reference:
            requisition = ClinicRequisition.objects.get(
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
        app_label = "bcpp_clinic_lab"
        verbose_name = 'Clinic Packing List Item'
