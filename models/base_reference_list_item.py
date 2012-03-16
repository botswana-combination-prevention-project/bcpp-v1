from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from bhp_common.models import MyBasicModel, MyBasicListModel
from bhp_common.choices import GENDER
from lab_common.choices import UNITS, ABS_CALC
from lab_test_code.models import TestCode
from lab_reference.choices import GENDER_OF_REFERENCE


class BaseReferenceListItem(MyBasicModel):

    test_code = models.ForeignKey(TestCode)

    gender = models.CharField(
        verbose_name = "Gender",
        choices = GENDER_OF_REFERENCE,
        max_length=10, 
        )
    lln = models.DecimalField(
        verbose_name = 'lower',
        null=True, 
        max_digits=12, 
        decimal_places=4, 
        blank=True)
    uln = models.DecimalField(
        verbose_name = 'upper',
        null=True, 
        max_digits=12, 
        decimal_places=4, 
        blank=True)
    age_low = models.IntegerField(
        null=True, 
        blank=True)
    age_low_unit = models.CharField(
        max_length=10, 
        blank=True
        )
    age_low_quantifier = models.CharField(max_length=10, blank=True)
    
    age_high = models.IntegerField(null=True, blank=True)
    
    age_high_unit = models.CharField(max_length=10, blank=True)
    
    age_high_quantifier = models.CharField(max_length=10, blank=True)
    
    panic_value_low = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    
    panic_value_high = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
      
    comment = models.CharField(
        verbose_name = "Comment", 
        max_length=250, 
        blank=True,
        )

    """
        lower |	upper
        ------|-------------
        m*30  |	(1+m)*30)-1
        y*365 |	(1+y)*365)-1 
    """

    """
    def age_low_days(self):
        if self.age_low_unit.upper() == 'D':
            days = self.age_low * 1
        elif self.age_low_unit.upper() == 'M':
            days = self.age_low * 30
        elif self.age_low_unit.upper() == 'Y':
            days = self.age_low * 365
        else:
            raise TypeError('Invalid age_low_unit in model TestCodeReference, You have the value \'%s\' stored' % (self.age_low_unit.upper()) )
        return days

    def age_high_days(self):
        if self.age_high_unit.upper() == 'D':
            days = self.age_high * 1
        elif self.age_high_unit.upper() == 'M':
            days = ((1+self.age_high) * 30)-1
        elif self.age_high_unit.upper() == 'Y':
            days = ((1+self.age_high) * 365)-1
        else:
            raise TypeError('Invalid age_high_unit in model TestCodeReference, You have the value \'%s\' stored' % (self.age_high_unit.upper()) )
        return days

    def __unicode__(self):
        return "%s" % (self.test_code)
    """
    
    class Meta:
        abstract = True
        app_label = 'bhp_lab_core'  
        ordering = ['test_code', 'age_low', 'age_low_unit']   
