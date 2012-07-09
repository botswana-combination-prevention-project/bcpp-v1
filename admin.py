from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_crypto.models import Crypt

class CryptAdmin (admin.ModelAdmin):

    list_display = (
        'cipher_text',
        )   

    search_fields = ('hash_text', 'cipher_text')    

    
    list_filter = ('hash_text',)
    
admin.site.register(Crypt, CryptAdmin)