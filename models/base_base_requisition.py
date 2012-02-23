from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.fields import InitialsField
from bhp_common.choices import YES_NO
from bhp_variables.models import StudySite
from lab_panel.models import Panel
from lab_aliquot_list.models import AliquotType
from lab_packing.models import PackingList
from lab_requisition.choices import PRIORITY, REASON_NOT_DRAWN, ITEM_TYPE
from lab_requisition.managers import BaseRequisitionManager


class BaseBaseRequisition (MyBasicUuidModel):
    
    """ does not include additional tests """
    
    requisition_identifier = models.CharField(
        verbose_name = 'Requisition Id',
        max_length = 25,
        )

    requisition_datetime =  models.DateTimeField(
        verbose_name='Requisition Date'
        )    
    
    specimen_identifier = models.CharField(
        verbose_name = 'Specimen Id',    
        max_length = 25,
        null = True,
        blank = True,
        editable = False
        )

    protocol = models.CharField(
        verbose_name = "Protocol Number",
        max_length=10,
        null = True,
        blank = True,
        help_text = 'Use three digit code e.g 041, 056, 062, etc'
        )

    site = models.ForeignKey(StudySite)    
    
    clinician_initials = InitialsField(
        default = '--',                               
        null = True,
        blank = True,
        )
    
    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)
    
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
        help_text = 'If not drawn, leave blank. Same as date and time of finger prick in case on DBS.',
        )

    item_type = models.CharField(
        verbose_name = 'Item collection type',
        max_length = 25,
        choices = ITEM_TYPE,
        default = 'tube',
        help_text = ''
        ) 

    item_count_total = models.IntegerField(
        verbose_name = 'Total number of items',
        default = 1,
        help_text = 'Number of tubes, samples, cards, etc being sent for this test/order only. Determines number of labels to print',
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
    
    is_receive = models.BooleanField(
        verbose_name = 'received',        
        default = False,
        )
    is_receive_datetime = models.DateTimeField(
        verbose_name = 'rcv-date',    
        null = True,
        blank = True,
        )

    is_packed = models.BooleanField(
        verbose_name = 'packed',    
        default = False,
        )

    is_labelled = models.BooleanField(
        verbose_name = 'labelled',
        default = False,
        )

    is_labelled_datetime = models.DateTimeField(
        verbose_name = 'label-date',
        null = True,
        blank = True,
        )
    
    is_lis = models.BooleanField(
        verbose_name = 'lis',    
        default = False,
        )
        
    packing_list = models.ForeignKey(PackingList, null=True)
    
    
    objects = BaseRequisitionManager()
    
    def __unicode__(self):
        return '%s' % (self.requisition_identifier)

    def save(self, *args, **kwargs):
    
        if self.is_drawn.lower() == 'yes':
            self.requisition_identifier = self.__class__.objects.get_identifier_for_device()
        
        #if not self.requisition_identifier:
        #    self.requisition_identifier = self.__class__.objects.get_identifier(site_code=self.site.site_code)
        
        return super(BaseBaseRequisition, self).save(*args, **kwargs)


    class Meta:
        abstract = True 
       
