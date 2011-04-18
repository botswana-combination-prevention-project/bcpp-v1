from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from bhp_lab_core.models import Order, Analyzer, TestCode
from bhp_lab_core.choices import RESULT_STATUS, RESULT_QUANTIFIER

class Result(MyBasicUuidModel):

    order = models.ForeignKey(Order)
    
    result_datetime = models.DateTimeField()

    assay_datetime = models.DateTimeField()

    #analyzer = models.ForeignKey(Analyzer)
    analyzer = models.CharField(max_length=50)
   
    source = models.CharField(
        verbose_name = 'Source',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = 'Reference to source of information, such as files name'
  	    )
    archive = models.CharField(
        verbose_name = 'Archive',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = 'Reference to archived file/location, if any'
  	    )

    comment = models.CharField(
        verbose_name = 'Comment',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
    
    #def __unicode__(self):
    #    return '%s :%s' % (self.order.order_number, self.result_datetime)
        
    class Meta:
        app_label = 'bhp_lab_core'    

class ResultItem(MyBasicUuidModel):

    result = models.ForeignKey(Result)

    #test_code = models.ForeignKey(TestCode)
    test_code = models.CharField(max_length=50)

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
       
