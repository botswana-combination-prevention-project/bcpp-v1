from django.db import models
#from django.db.models.signals import post_save, m2m_changed
#from django.dispatch import receiver
from django.core import serializers

from bhp_common.models import MyBasicUuidModel
from bhp_sync.classes import TransactionProducer


class TransactionManager(models.Manager):
    
    pass
