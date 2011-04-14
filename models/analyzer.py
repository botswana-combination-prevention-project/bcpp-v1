from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from bhp_lab_core.models import Panel

class Analyzer(MyBasicUuidModel):

    name = models.CharField(
        verbose_name = 'Common name',
	    max_length = 15,
	    help_text = ''
  	    )
    serial_number = models.CharField(
        verbose_name = 'Serial number',
	    max_length = 25,
	    help_text = ''
  	    )

    make = models.CharField(
        verbose_name = 'Make',
	    max_length = 25,
	    help_text = ''
  	    )

    model = models.CharField(
        verbose_name = 'Model',
	    max_length = 25,
	    help_text = ''
  	    )

    panel = models.ManyToManyField(Panel,
        help_text = 'Analyzer can run these panels'
        )
    
    class Meta:
        app_label = 'bhp_lab' 
        

