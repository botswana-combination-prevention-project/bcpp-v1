from django.contrib import admin
from bhp_crypto.models import Crypt


class CryptAdmin (admin.ModelAdmin):

    list_display = ('hash',)
    search_fields = ('hash',)

admin.site.register(Crypt, CryptAdmin)
