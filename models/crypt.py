from django.db import models
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel


class Crypt (BaseUuidModel):

    hash_text = models.CharField(
        verbose_name = "Hash",
        max_length = 128,
        db_index=True,
        unique=True,
        ) 
    
    cipher_text = models.TextField(
        verbose_name = "Cipher",
        ) 
    
    class Meta:
        app_label = 'bhp_crypto'
        verbose_name = 'Crypt'
        
    
    