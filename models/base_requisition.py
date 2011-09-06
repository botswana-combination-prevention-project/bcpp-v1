from django.db import models
from django.conf import settings
from bhp_identifier.classes import Identifier
from bhp_common.models import MyBasicUuidModel
from bhp_common.fields import InitialsField
from bhp_common.choices import YES_NO
from bhp_variables.models import StudySite
from bhp_registration.models import RegisteredSubject
from bhp_variables.models import StudySite, StudySpecific
from lab_panel.models import Panel
from lab_aliquot_list.models import AliquotType
from lab_test_code.models import TestCode
from lab_requisition.choices import PRIORITY, REASON_NOT_DRAWN, ITEM_TYPE
from lab_requisition.classes import ClinicRequisitionLabel


class BaseRequisitionManager(models.Manager):

    def get_identifier(self, **kwargs):

        site_code = kwargs.get('site_code')        

        if not site_code:
            try:
                site_code = settings.SITE_CODE
            except AttributeError:
                raise AttributeError('Requisition needs a \'site_code\'. Got None. Either pass as a parameter or set SITE_CODE= in settings.py')

        if len(site_code) == 1:
            site_code = site_code + '0'
        return Identifier(subject_type = 'requisition', site_code=site_code).create()

class BaseRequisition (MyBasicUuidModel):
    
    requisition_identifier = models.CharField(
        max_length = 25,
        )

    requisition_datetime =  models.DateTimeField(
        verbose_name='Requisition Date / Time'
        )    
    
    protocol = models.CharField(
        verbose_name = "Protocol Number",
        max_length=10,
        null = True,
        blank = True,
        )

    site = models.ForeignKey(StudySite)    
    
    clinician_initials = InitialsField()
    
    aliquot_type = models.ForeignKey(AliquotType,
        default = AliquotType.objects.filter(alpha_code='WB')[0],
        )

    panel = models.ForeignKey(Panel)
    
    # populate this one based on the selected panel at the dashboard
    test_code = models.ManyToManyField(TestCode,
        verbose_name = 'Additional tests',
        null = True,
        blank = True,
        )
    
    priority = models.CharField(
        verbose_name = 'Priority',
        max_length = 25,
        choices = PRIORITY,
        default = 'normal',
        )
    
    is_drawn = models.CharField(
        verbose_name = 'Was a specimen drawn?',
        max_length = 3,
        choices = YES_NO,
        default = 'Yes',
        help_text = 'If No, provide a reason below'
        )
        
    reason_not_drawn = models.CharField(
        verbose_name = 'If not drawn, please explain',
        max_length = 25,
        choices = REASON_NOT_DRAWN,
        null = True,
        blank = True,
        )            

    drawn_datetime =  models.DateTimeField(
        verbose_name = 'Date / Time Specimen Drawn',
        null = True,
        blank = True,
        help_text = 'If not drawn, leave blank',
        )

    item_type = models.CharField(
        verbose_name = 'Collection type',
        max_length = 25,
        choices = ITEM_TYPE,
        default = 'tube',
        ) 

    item_count_total = models.IntegerField(
        verbose_name = 'Total Number of tubes',
        default = 1,
        help_text = 'Number of tubes, samples, etc being sent for this test/order only. Determines number of labels to print',
        ) 
    
    estimated_volume = models.DecimalField(
        verbose_name = 'Estimated volume in mL',
        max_digits = 7,
        decimal_places = 1,
        default = 5.0,
        help_text = 'If applicable, estimated volume of sample for this test/order. This is the total volume if number of "tubes" above is greater than 1'
        )
        
    
    comments = models.TextField(
        max_length=25,
        null = True,
        blank = True,
        )
    
    objects = BaseRequisitionManager()
    
    def __unicode__(self):
        return '%s' % (self.requisition_identifier)

    def save(self, *args, **kwargs):
    
        if not self.requisition_identifier:
            self.requisition_identifier = self.__class__.objects.get_identifier(site_code=self.site.site_code)
        
        
        for cnt in range(self.item_count_total, 0, -1):
            label = ClinicRequisitionLabel(
                            item_count = cnt, 
                            requisition = self,
                            )
            label.print_label() 
                                       
        return super(BaseRequisition, self).save(*args, **kwargs)


    class Meta:
        abstract = True 
       
