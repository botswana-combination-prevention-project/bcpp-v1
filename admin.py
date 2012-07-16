from django.contrib import admin
from bhp_crypto.models import Crypt
#from bhp_crypto.models import TestModel

class CryptAdmin (admin.ModelAdmin):

    list_display = ('hash',)   

    search_fields = ('hash',)    
    
admin.site.register(Crypt, CryptAdmin)

#class TestModelAdmin (admin.ModelAdmin):
#    pass
#admin.site.register(TestModel, TestModelAdmin)