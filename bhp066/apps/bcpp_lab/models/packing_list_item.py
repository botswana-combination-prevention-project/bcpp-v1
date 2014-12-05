from django.db import models

from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_packing.models import BasePackingListItem

from .aliquot import Aliquot
from .packing_list import PackingList
from .panel import Panel
from .subject_requisition import SubjectRequisition

from ..managers import PackingListItemManager


class PackingListItem(BasePackingListItem):

    packing_list = models.ForeignKey(PackingList, null=True)

    panel = models.ForeignKey(Panel,
        null=True,
        blank=True,
        )

    objects = PackingListItemManager()

    def save(self, *args, **kwargs):
        try:
            self.panel = self.subject_requisition.panel
            self.item_datetime = self.subject_requisition.drawn_datetime
        except AttributeError:
            pass
        super(PackingListItem, self).save(*args, **kwargs)

    @property
    def subject_requisition(self):
        """Returns the SubjectRequisition either directly or via the
        Aliquot."""
        try:
            return SubjectRequisition.objects.get(pk=self.requisition)
        except SubjectRequisition.DoesNotExist:
            aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
            return SubjectRequisition.objects.get(
                requisition_identifier=aliquot.receive.requisition_identifier)

    @property
    def drawn_datetime(self):
        """Returns the sample datetime drawn from the SubjectRequisition."""
        return self.subject_requisition.drawn_datetime

    def clinician(self):
        retval = "n/a"
        if self.item_reference:
            aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
            requisition = SubjectRequisition.objects.get(
                requisition_identifier=aliquot.receive.requisition_identifier
                )
            retval = requisition.user_created
        return retval

    def gender(self):
        retval = "n/a"
        if self.item_reference:
            aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
            requisition = SubjectRequisition.objects.get(
                requisition_identifier=aliquot.receive.requisition_identifier
                )
            subject_identifier = requisition.subject()
            if subject_identifier:
                registered_subject = RegisteredSubject.objects.get(
                    subject_identifier=subject_identifier
                    )
                retval = registered_subject.gender
        return retval

    def natural_key(self):
        return (self.item_reference, )

    class Meta:
        app_label = "bcpp_lab"
        verbose_name = 'Packing List Item'
