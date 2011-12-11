from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel
from lab_account.models import AccountHolder

class Account (MyBasicUuidModel):
    
    account_name = models.CharField(
        max_length = 25,
        unique = True,
        )
        
    account_opendate = models.DateField(
        verbose_name = 'Open date',
        )    

    account_closedate = models.DateField(
        verbose_name = 'Closed date',
        )    

    account_holder = models.ForeignKey(AccountHolder,
    	null = True,
    	blank = True,
    	)

    comment = models.CharField("Comment", 
        max_length = 250, 
        blank = True,
        )        
               
    def get_absolute_url(self):
        return "/lab_account/account/%s/" % self.id   

    def __unicode__(self):
        return self.account_name
        
    class Meta:
        ordering = ["account_name"]
        app_label = 'lab_account'
        db_table = 'bhp_lab_registration_account'                        

