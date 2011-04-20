from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel, MyBasicListModel
from bhp_lab_core.models import Order, Analyzer, TestCode
from bhp_lab_core.choices import RESULT_STATUS, RESULT_QUANTIFIER


class ResultSource(MyBasicListModel):
    pass

    class Meta:
        app_label = 'bhp_lab_core'    


class Result(MyBasicUuidModel):

    result_identifier = models.CharField(
        max_length=25,
        editable=False,
        )

    order = models.ForeignKey(Order)
    
    result_datetime = models.DateTimeField(
        help_text = 'Date result was added to system.',
        )

    assay_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text = 'Min date of all results associtaed with result',
        )

    result_source = models.ForeignKey(ResultSource,
        verbose_name = 'Source',
	    help_text = 'Reference to source of information, such as interface, manual, outside lab, ...'
  	    )

    result_source_reference = models.CharField(
        verbose_name = 'Source Reference',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = 'Reference to source, invoice, filename, machine, etc'
  	    )

    comment = models.CharField(
        verbose_name = 'Comment',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
    
    def __unicode__(self):
        return '%s' % (self.result_identifier)
        
    class Meta:
        app_label = 'bhp_lab_core'    

class ResultItem(MyBasicUuidModel):

    result = models.ForeignKey(Result)

    test_code = models.ForeignKey(TestCode)

    result_value = models.CharField(
        verbose_name = 'Result',
	    max_length = 25,
	    help_text = ''
	    )

    result_quantifier = models.CharField(
        verbose_name = 'Quantifier',
        default = '=',
        choices = RESULT_QUANTIFIER,
	    max_length = 25,
	    help_text = ''
	    )
	    
    status = models.CharField(
        verbose_name = 'Status',
        default = 'P',
        choices = RESULT_STATUS,
	    max_length = 10,
	    help_text = 'Default is preliminary'
	    )
    result_item_source = models.CharField(
        max_length=25,
        verbose_name = 'Source',
	    null = True,
        blank = True,	    
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
    comment = models.CharField(
        verbose_name = 'Comment',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
  	
    class Meta:
        app_label = 'bhp_lab_core'    
       
