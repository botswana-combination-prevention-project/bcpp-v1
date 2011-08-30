from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from lab_order.models import Order
from lab_result.choices import RESULT_RELEASE_STATUS


class Result(MyBasicUuidModel):

    result_identifier = models.CharField(
        max_length=25,
        editable=False,
        db_index=True,        
        )

    order = models.ForeignKey(Order)
    
    result_datetime = models.DateTimeField(
        help_text = 'Date result added to system.',
        db_index=True,        
        )

    release_status = models.CharField(
        max_length=25,
        choices=RESULT_RELEASE_STATUS,
        default='NEW',
        db_index=True,        
        )

    release_datetime = models.DateTimeField(
  	    null = True,
        blank = True,	    
        help_text = 'Date result authorized for release. This field will auto-fill if release status is changed',
        db_index=True,        
        )
    
    release_username = models.CharField(
        verbose_name = "Release username",
        max_length=50,
	    null=True,
	    blank=True,
        help_text = 'Username of person authorizing result for release. This field will auto-fill if release status is changed',        	    
        db_index=True,        
	    )

    comment = models.CharField(
        verbose_name = 'Comment',
	    max_length = 50,
	    null = True,
        blank = True,	    
	    help_text = ''
  	    )
  	    
    dmis_result_guid = models.CharField(
        max_length=36,
	    null = True,
        blank = True,	
        #editable=False,            
	    help_text = 'dmis import value. N/A unless data imported from old system'
        )  	    
    
    def __unicode__(self):
        return '%s' % (self.result_identifier)

    def get_absolute_url(self):
        return "/lab_result/result/%s/" % self.id   
        
    def get_search_url(self):
        return "/laboratory/result/search/result/%s/" % self.result_identifier   

    def get_document_url(self):
        return "/laboratory/result/document/%s/" % (self.result_identifier)  	

    class Meta:
        app_label = 'lab_result' 
        db_table = 'bhp_lab_core_result'
        ordering =['result_identifier','order','result_datetime',]  
