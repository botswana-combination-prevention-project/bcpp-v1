from django.db import models
#from audit_trail.audit import AuditTrail
from lab_result.models import Result, ResultSource
from lab_test_code.models import TestCode
from lab_result_item.classes import ReferenceRangeFlag, GradeFlag
from base_result_item import BaseResultItem


class ResultItem(BaseResultItem):

    test_code = models.ForeignKey(TestCode)

    result = models.ForeignKey(Result)

    result_item_source = models.ForeignKey(ResultSource,
        verbose_name='Source',
        help_text='Reference to source of information, such as interface, manual, outside lab, ...',
        db_index=True)

    result_item_source_reference = models.CharField(
        verbose_name='Source Reference',
        max_length=50,
        null=True,
        blank=True,
        help_text='Reference to source, invoice, filename, machine, etc')
    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")
    receive_identifier = models.CharField(
        max_length=25, editable=False, null=True, db_index=True,
        help_text="non-user helper field to simplify search and filter")
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.result.order.aliquot.registered_subject.subject_identifier
        self.receive_identifier = self.result.order.aliquot.receive.receive_identifier
        super(ResultItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s' % (unicode(self.result), unicode(self.test_code))

    def get_cls_reference_flag(self):
        return ReferenceRangeFlag

    def get_cls_grade_flag(self):
        return GradeFlag

    def get_absolute_url(self):
        return "lab_result_item/resultitem/%s/" % (self.id)

    def get_result_document_url(self):
        return "/laboratory/result/document/%s/" % (self.result.result_identifier)

    #TODO: get this to return a subject_identifier for the audit trial
    def get_subject_identifier(self,):
        return ''

    class Meta:
        app_label = 'lab_result_item'
        db_table = 'bhp_lab_core_resultitem'
