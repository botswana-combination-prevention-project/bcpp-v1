from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin, BaseTabularInline
from models import ConsentCatalogue, AttachedModel
from forms import ConsentCatalogueForm


class AttachedModelInlineAdmin(BaseTabularInline):
    model = AttachedModel
    extra = 1


class ConsentCatalogueAdmin(BaseModelAdmin):
    form = ConsentCatalogueForm
    list_display = ('name', 'version', 'consent_type', 'start_datetime', 'end_datetime')
    list_filter = ('consent_type', 'created')
    inlines = [AttachedModelInlineAdmin, ]
admin.site.register(ConsentCatalogue, ConsentCatalogueAdmin)
