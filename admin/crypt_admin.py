from django.contrib import admin
from bhp_crypto.models import Crypt, TestModel


class CryptAdmin (admin.ModelAdmin):

    list_display = ('hash', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('hash',)

admin.site.register(Crypt, CryptAdmin)


class TestModelAdmin (admin.ModelAdmin):

    list_display = ('firstname', 'lastname')
    search_fields = ('firstname', 'lastname')

admin.site.register(TestModel, TestModelAdmin)
