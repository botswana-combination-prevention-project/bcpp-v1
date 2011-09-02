from django.db import models
from django.conf import settings
from bhp_identifier.classes import Identifier
from bhp_common.models import MyBasicUuidModel
from bhp_common.fields import InitialsField
from bhp_variables.models import StudySite
from bhp_registration.models import RegisteredSubject
from bhp_variables.models import StudySite, StudySpecific
from lab_panel.models import Panel
from lab_test_code.models import TestCode
from bhp_lab_api.choices import PRIORITY

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

    #registered_subject = models.ForeignKey(RegisteredSubject,
    ##    #editable = False,
    #   )
    
    drawn_datetime =  models.DateTimeField()
    
    # visit should be limited to those that exist for this patient
    # visit_definition = models.ForeignKey(VisitDefinition)

    protocol = models.CharField(
        verbose_name = "BHP Protocol Number",
        max_length=10,
        null = True,
        blank = True,
        )

    site = models.ForeignKey(StudySite)    
    
    panel = models.ForeignKey(Panel)
    
    # populate this one based on the selected panel at the dashboard
    test_code = models.ManyToManyField(TestCode,
        null = True,
        blank = True,
        )
    
    priority = models.CharField(
        verbose_name = 'Priority',
        max_length = 25,
        choices = PRIORITY,
        default = 'normal',
        )
    
    clinician_initials = InitialsField()
    
    comments = models.TextField(
        max_length=25,
        null = True,
        blank = True,
        )
    
    objects = BaseRequisitionManager()
    
    def __unicode__(self):
        return '%s' % (self.requisition_identifier)

    def save(self, *args, **kwargs):
    
        #self.registered_subject = self.visit.appointment.registered_subject   
        
        #if not self.panel:
        #    self.panel = self.__class__._meta.module_name
        
        self.requisition_identifier = self.__class__.objects.get_identifier(site_code=self.site.site_code)
        
        return super(BaseRequisition, self).save(*args, **kwargs)


    class Meta:
        abstract = True 
        

