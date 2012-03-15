import re
from django.db import models
from bhp_common.models import MyBasicUuidModel
from lab_result_item.choices import RESULT_VALIDATION_STATUS, RESULT_QUANTIFIER


class BaseResultItem(MyBasicUuidModel):

    result_item_value = models.CharField(
        verbose_name = 'Result',
	    max_length = 25,
	    help_text = '',
        db_index=True,
	    )

    result_item_value_as_float = models.FloatField(
        verbose_name = 'Result as float',
        #max_digits = 15,
        help_text = '',
        null = True,
        db_index=True,
        editable = False,
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

    grade_range = models.CharField(
        max_length = 25,
        null = True,
        blank = True,
        )

    grade_flag = models.CharField(
        max_length = 5,
        null = True,
        blank = True,
        )

    reference_flag = models.CharField(
        max_length = 5,
        null = True,
        blank = True,
        )  
    
    reference_range = models.CharField(
        max_length = 25,
        null = True,
        blank = True,
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

    error_code = models.CharField(
        verbose_name = 'Error codes',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )

    def get_subject_identifier(self):
        return ''
    
    def save(self, *args, **kwargs):
        
        # if value can be converted to a numeric, then do so and store as float
        if re.search(r'\d+\.?\d*', self.result_item_value):
            try:
                self.result_item_value_as_float = float(self.result_item_value)
            except:
                self.result_item_value_as_float = None    
            
        super(BaseResultItem, self).save(*args, **kwargs)

    
    class Meta:
        abstract = True       
