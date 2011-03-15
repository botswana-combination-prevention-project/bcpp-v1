from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from bhp_lab.models import Order, Analyzer, Test
from bhp_lab.choices import RESULT_STATUS, RESULT_QUANTIFIER

class Result(MyBasicUuidModel):
    order = models.ForeignKey(Order)
    
    class Meta:
        app_label = 'bhp_lab'    

class ResultItem(MyBasicUuidModel):

    result = models.ForeignKey(Result)

    test = models.ForeignKey(Test)

    assay_date = models.DateTimeField()

    result = models.CharField(
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
	
    analyzer = models.ForeignKey(Analyzer)
    
    error_code = models.CharField(
        verbose_name = 'Error codes',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
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
        verbose_name = 'Error codes',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
  	
    class Meta:
        app_label = 'bhp_lab'    
       
