from django.db import models
from bhp_base_model.classes import BaseUuidModel

class Crypt (BaseUuidModel):

    hash_text = models.TextField(
        verbose_name = "Hash",
        ) 
    
    cipher_text = models.TextField(
        verbose_name = "Cipher",
        ) 
    
    class Meta:
        app_label = 'bhp_crypto'
        verbose_name = 'Crypt'
        
    
    