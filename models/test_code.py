from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from bhp_common.models import MyBasicModel, MyBasicListModel
from bhp_common.choices import GENDER
from bhp_lab_core.choices import UNITS, ABS_CALC
    
class TestCodeGroup(MyBasicModel):
    
    code = models.CharField(
        max_length=3
        )
    name = models.CharField(
        max_length = 25,
        null=True,
        blank=True,
        )
    
    def __unicode__(self):
        return self.code    
    class Meta:
        app_label = 'bhp_lab_core'            


class TestCode(MyBasicModel):

    code = models.CharField(
        verbose_name = "Test Code", 
        max_length=15, 
        unique=True,
        validators = [
            RegexValidator('^[A-Z0-9\%\_]{1,15}$', 'Ensure test code is uppercase alphanumeric ( with _ ,%) and no spaces'),
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

    reference_range_hi = models.DecimalField(
        verbose_name = 'Ref. Range Hi',
        decimal_places = 4,
        max_digits = 10,
        )

    reference_range_lo = models.DecimalField(
        verbose_name = 'Ref. Range Lo',
        decimal_places = 4,
        max_digits = 10,
        )
    
    lln = models.DecimalField(
        verbose_name = 'LLN',
        decimal_places = 4,
        max_digits = 10,
        null = True,
        blank = True,        
        )

    uln = models.DecimalField(
        verbose_name = 'ULN',
        decimal_places = 4,
        max_digits = 10,
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
        verbose_name = 'If calulated, formula?',
        max_length = '50',
        null = True,
        blank = True,
        )

    def __unicode__(self):
        return "%s" % (self.name)
        
    class Meta:
        ordering = ['name']
        app_label = 'bhp_lab_core'     
        
class TestCodeReference(MyBasicModel):

    test_code = models.ForeignKey(TestCode)

    gender = models.CharField(
        verbose_name = "Gender",
        choices = GENDER,
        max_length=10, 
        )

    age_low = models.DecimalField(
        null=True, 
        max_digits=12, 
        decimal_places=4, 
        blank=True)
    age_low_unit = models.CharField(
        max_length=75, 
        blank=True
        )

    age_low_quantifier = models.CharField(max_length=75, blank=True)
    
    age_high = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    
    age_high_unit = models.CharField(max_length=75, blank=True)
    
    age_high_quantifier = models.CharField(max_length=75, blank=True)
    
    panic_value = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    
    panic_value_quantifier = models.CharField(max_length=75, blank=True)
        
    comment = models.CharField(
        verbose_name = "Comment", 
        max_length=250, 
        blank=True,
        )

    def __unicode__(self):
        return "%s" % (self.test_code)
        
    class Meta:
        app_label = 'bhp_lab_core'     
        
class TestCodeInterfaceMapping(MyBasicModel):

    foreign_test_code = models.CharField(
        verbose_name = "Foreign Test Code", 
        max_length=15, 
        unique=True,
        )
        
    local_test_code = models.ForeignKey(TestCode,
        verbose_name = "Local Test Code", 
        )

    def __unicode__(self):
        return "%s maps to %s" % (self.foreign_test_code,self.local_test_code)

    class Meta:
        app_label = 'bhp_lab_core'            

           
