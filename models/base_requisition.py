from django.db import models
from django.conf import settings
from bhp_identifier.classes import Identifier
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
from lab_requisition.managers import BaseRequisitionManager
from base_base_requisition import BaseBaseRequisition

class BaseRequisition (BaseBaseRequisition):
    
    # populate this one based on the selected panel at the dashboard
    test_code = models.ManyToManyField(TestCode,
        verbose_name = 'Additional tests',
        null = True,
        blank = True,
        )
    
    class Meta:
        abstract = True 
       
