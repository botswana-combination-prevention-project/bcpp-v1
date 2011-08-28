from django.db import models
from django_extensions.db.models import TimeStampedModel
from bhp_common.fields import HostnameCreationField, HostnameModificationField


class MyBasicModel(TimeStampedModel):

    """Base model class for all models. Adds created and modified values for user, date and hostname (computer)"""
    
    user_created = models.CharField(max_length=250, verbose_name='user created', editable=False, default="")
    
    user_modified = models.CharField(max_length=250, verbose_name='user modified',editable=False, default="")
    
    hostname_created = HostnameCreationField()
    
    hostname_modified = HostnameModificationField()
    
    class Meta:
        abstract = True
