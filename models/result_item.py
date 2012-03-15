from django.db import models
#from audit_trail.audit import AuditTrail
from lab_reference.classes import ReferenceFlag
from lab_grading.classes import GradeFlag
from lab_result.models import Result, ResultSource
from lab_test_code.models import TestCode
from base_result_item import BaseResultItem


class ResultItem(BaseResultItem):

    test_code = models.ForeignKey(TestCode)

    result = models.ForeignKey(Result)

    result_item_source = models.ForeignKey(ResultSource,
        verbose_name = 'Source',
	    help_text = 'Reference to source of information, such as interface, manual, outside lab, ...',
	    db_index = True,
  	    )

    result_item_source_reference = models.CharField(
        verbose_name = 'Source Reference',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = 'Reference to source, invoice, filename, machine, etc'
  	    )


    #history = AuditTrail()
    
    def save(self, *args, **kwargs):
        
        reference = ReferenceFlag()
        reference.dob = self.result.order.aliquot.receive.patient.dob
        reference.gender = self.result.order.aliquot.receive.patient.gender
        reference.drawn_datetime = self.result.order.aliquot.receive.drawn_datetime
        reference.test_code = self.test_code
        if reference.flag:
            self.reference_range = '%s - %s' % (reference.flag['range']['lln'], reference.flag['range']['uln'])
            self.reference_flag = reference.flag['flag']        

        grade = GradeFlag()
        grade.dob = self.result.order.aliquot.receive.patient.dob
        grade.gender = self.result.order.aliquot.receive.patient.gender
        grade.drawn_datetime = self.result.order.aliquot.receive.drawn_datetime
        grade.test_code = self.test_code
        if grade.flag:
            self.grade_range = '%s - %s' % (grade.flag['range']['lln'], grade.flag['range']['uln'])
            self.grade_flag = grade.flag['flag']        

        return super(ResultItem, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return '%s %s' % (unicode(self.result), unicode(self.test_code))
    
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
            
       
       

