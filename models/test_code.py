from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from bhp_common.models import MyBasicModel, MyBasicListModel
from bhp_common.choices import GENDER
from bhp_lab_common.choices import UNITS, ABS_CALC
from bhp_lab_test_code.models import TestCodeGroup
    
class TestCode(MyBasicModel):

    code = models.CharField(
        verbose_name = "Test Code", 
        max_length=15, 
        unique=True,
        validators = [
            RegexValidator('^[A-Z0-9\%\_\-]{1,15}$', 'Ensure test code is uppercase alphanumeric ( with _ ,%) and no spaces'),
            ],
        )
        
    name = models.CharField(
        verbose_name = "Test Code Description", 
        max_length=50,
        )

    test_code_group = models.ForeignKey(TestCodeGroup)
    
    units = models.CharField(
        verbose_name = 'Units',
        max_length = 25,
        choices = UNITS,
        )
        
    display_decimal_places = models.IntegerField(
        verbose_name = 'Decimal places to display',
        null = True,
        blank = True,        
        )

    is_absolute = models.CharField(
        verbose_name = 'Is the value absolute or calculated?',
        max_length = '15',
        default = 'absolute',
        choices = ABS_CALC,
        )
        
    formula = models.CharField(
        verbose_name = 'If calculated, formula?',
        max_length = '50',
        null = True,
        blank = True,
        )

    def __unicode__(self):
        return "%s" % (self.name)
        
    class Meta:
        ordering = ['name']
        app_label = 'bhp_lab_test_code'     
        

        

