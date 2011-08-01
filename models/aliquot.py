import datetime
from django.db import models
from django.core.validators import RegexValidator
from bhp_common.models import MyBasicUuidModel, MyBasicListModel, MyBasicModel
from bhp_lab_core.choices import ALIQUOT_STATUS
from bhp_lab_core.choices import SPECIMEN_MEASURE_UNITS, SPECIMEN_MEDIUM
from bhp_lab_core.models import Receive


class AliquotManager(models.Manager):
    
    def format_identifier(self, **kwargs):

        receive = kwargs.get('receive')
        aliquot_type = kwargs.get('aliquot_type')            
        parent_aliquot = kwargs.get('parent_aliquot')
                   
        if parent_aliquot:
            parent_segment = str(parent_aliquot.aliquot_type.numeric_code).rjust(2,'0') + str(parent_aliquot.count).rjust(2,'0')
            self_count = parent_aliquot.count + 1            
        else:
            parent_segment = ''.rjust(4,'0')  
            self_count = 1
        
        # todo: might be a good place to do a sanity check on 'parent' to 'self' aliquot type
        
        self_segment = aliquot_type.numeric_code.rjust(2,'0') + str(self_count).rjust(2,'0')
        
        return '%s%s%s' % (receive.receive_identifier, parent_segment, self_segment)
    
    def get_identifier(self, **kwargs):
    
        """
a=Aliquot.objects.all()[10]
Aliquot.objects.create_aliquot(receive=a.receive, aliquot_type=a.aliquot_type, parent_identifier=a.aliquot_identifier)    
        """
        receive = kwargs.get('receive')
        if not receive:
            raise TypeError('AliquotManager.create_aliquot needs a receiving record. Got none.')

        aliquot_type = kwargs.get('aliquot_type')
        if not aliquot_type:
            raise TypeError('AliquotManager.create_aliquot needs an aliquot_type. Got none.')

        study_specific = StudySpecific.objects.all()[0]

        qset = Q()
       
        parent_identifier = kwargs.get('parent_identifier') 

        if parent_identifier:
            qset.add(Q(aliquot_identifier = parent_identifier), Q.AND)
            parent_aliquot = super(AliquotManager, self).filter(qset).order_by('-count')[0]
        else:    
            parent_aliquot = super(AliquotManager, self).none()
            
        if parent_identifier and not parent_aliquot:
            # you specified a parent but it does not exist, abandon...
            aliquot_identifier = ''
        else:    
            # create a new primary aliquot OR a child aliquot
            if parent_aliquot:
                # create a child
                aliquot_identifier = self._format_identifier(
                            receive = receive,
                            parent_aliquot = parent_aliquot,
                            aliquot_type = aliquot_type,
                        )
                
            else:
                # create a new aliquot (primary)    
                aliquot_identifier = self._format_identifier(
                            receive = receive,
                            aliquot_type = aliquot_type,
                        )

        return aliquot_identifier

class AliquotMedium(MyBasicListModel):

    def __unicode__(self):
        return "%s" % ( self.name.upper())
    class Meta:
        ordering = ["name"]
        app_label = 'bhp_lab_core'        


class AliquotType(MyBasicModel):

    name = models.CharField(
        verbose_name = 'Description',
        max_length=50,        
        )
    
    alpha_code = models.CharField(
        verbose_name = 'Aplha code',
        validators = [
            RegexValidator('^[A-Z]{2,15}$')
            ],
        max_length=15,
        unique=True,        
        )
    numeric_code = models.CharField(
        verbose_name = 'Numeric code (2-digit)',
        max_length = 2,
        validators = [
            RegexValidator('^[0-9]{2}$')
            ],
        unique=True,    
        )
        
    dmis_reference = models.IntegerField()        
    
    def __unicode__(self):
        return "%s: %s" % ( self.numeric_code, self.name.lower())

    class Meta:
        ordering = ["name"]
        app_label = 'bhp_lab_core'        
        
class AliquotCondition(MyBasicListModel):
    
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)
    class Meta:
        ordering = ["short_name"]
        app_label = 'bhp_lab_core'        


class Aliquot (MyBasicUuidModel):
    
    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier', 
        max_length=25, 
        unique=True, 
        help_text="Aliquot identifier", 
        editable=False,
        )
        
    aliquot_datetime = models.DateTimeField(
        verbose_name = "Date and time aliquot created",
        default = datetime.datetime.today(),
        )
    
    receive = models.ForeignKey(Receive)
        
    count = models.IntegerField(
        editable=False,
        null=True
        )
        
    parent_identifier = models.ForeignKey('self',
        to_field = 'aliquot_identifier',
        blank=True,
        null=True,
        )
    
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        )
        
    medium  = models.CharField(
        verbose_name = 'Medium',
        max_length = 25,        
        choices = SPECIMEN_MEDIUM,
        default = 'TUBE',
        #help_text = "Indicate such as dbs card, tube, swab, etc",
        )
  
    original_measure  = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default = '5.00',
        )

    current_measure  = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default = '5.00',
        )

    measure_units = models.CharField(
        max_length = 25,
        choices=SPECIMEN_MEASURE_UNITS,
        default = 'mL',
        )

        
    condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        default = 10,
        )
        
    status = models.CharField(
        max_length = 25,
        choices = ALIQUOT_STATUS,
        default = 'available',
        )
        
    comment = models.CharField(
        max_length = 50,
        null=True,
        blank=True,
        )
    
    objects = AliquotManager()

  
    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    def get_absolute_url(self):
        return "/bhp_lab_core/aliquot/%s/" % self.id   
        
    def get_search_url(self):
        return "/laboratory/aliquot/search/aliquot/byword/%s/" % self.id   

    class Meta:
        app_label = 'bhp_lab_core'

  
