from django.contrib import admin
from bhp_crypto.models import Crypt
from bhp_crypto.models import TestModel

class CryptAdmin (admin.ModelAdmin):

    list_display = (
        'cipher_text',
        )   

    search_fields = ('hash_text', 'cipher_text')    

    
    list_filter = ('hash_text',)
    
admin.site.register(Crypt, CryptAdmin)

class TestModelAdmin (admin.ModelAdmin):
    pass
admin.site.register(TestModel, TestModelAdmin)