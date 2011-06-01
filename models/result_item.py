from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from bhp_lab_core.models import Result, TestCode, ResultSource
from bhp_lab_core.choices import RESULT_VALIDATION_STATUS, RESULT_QUANTIFIER
from audit_trail import audit


class ResultItem(MyBasicUuidModel):

    result = models.ForeignKey(Result)

    test_code = models.ForeignKey(TestCode)

    result_item_value = models.CharField(
        verbose_name = 'Result',
	    max_length = 25,
	    help_text = '',
        db_index=True,
	    )

    result_item_quantifier = models.CharField(
        verbose_name = 'Quantifier',
        default = '=',
        choices = RESULT_QUANTIFIER,
	    max_length = 25,
	    help_text = '',
	    )
    
    result_item_datetime = models.DateTimeField(
        verbose_name = 'Assay date and time',
        db_index=True,        
        )
    result_item_operator = models.CharField(
        verbose_name = 'Operator',
        max_length=50,
	    null=True,
	    blank=True,
        db_index=True,	    
        )

    validation_status = models.CharField(
        verbose_name = 'Status',
        default = 'P',
        choices = RESULT_VALIDATION_STATUS,
	    max_length = 10,
	    help_text = 'Default is preliminary',
        db_index=True,	    
	    )

    validation_datetime = models.DateTimeField(
	    null=True,
	    blank=True,
        db_index=True,	    
	    )
	
    validation_username = models.CharField(
        verbose_name = "Validation username",
        max_length=50,
	    null=True,
	    blank=True,
        db_index=True,	    
	    )
    validation_reference = models.CharField(
        verbose_name = "Validation reference",
        max_length=50,
	    null=True,
	    blank=True,
	    )

    comment = models.CharField(
        verbose_name = 'Validation Comment',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )

    result_item_source = models.ForeignKey(ResultSource,
        verbose_name = 'Source',
	    help_text = 'Reference to source of information, such as interface, manual, outside lab, ...'
  	    )

    result_item_source_reference = models.CharField(
        verbose_name = 'Source Reference',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = 'Reference to source, invoice, filename, machine, etc'
  	    )

    
    error_code = models.CharField(
        verbose_name = 'Error codes',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
  	    
    history = audit.AuditTrail()
  	    
    def __unicode__(self):
  	    return '%s %s' % (unicode(self.result), unicode(self.test_code))
    def get_absolute_url(self):
        return "bhp_lab_core/resultitem/%s/" % (self.id)
    def get_result_document_url(self):
        return "/laboratory/result/document/%s/" % (self.result.result_identifier)  	
    class Meta:
        app_label = 'bhp_lab_core'    
       
