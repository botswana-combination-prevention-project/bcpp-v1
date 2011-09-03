from django.db import models
from django.utils.translation import ugettext_lazy as _
from audit_trail.audit import AuditTrail
from lab_result.models import Result, ResultSource
from base_result_item import BaseResultItem


class ResultItem(BaseResultItem):

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


    history = AuditTrail()
  	    
    def __unicode__(self):
  	    return '%s %s' % (unicode(self.result), unicode(self.test_code))
    def get_absolute_url(self):
        return "lab_result_item/resultitem/%s/" % (self.id)
    def get_result_document_url(self):
        return "/laboratory/result/document/%s/" % (self.result.result_identifier)  	
    class Meta:
        app_label = 'lab_result_item'    
        db_table = 'bhp_lab_core_resultitem'            
            
       
