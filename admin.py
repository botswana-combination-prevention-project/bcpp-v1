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
    #inlines = [AttachedModelInlineAdmin, ]
admin.site.register(ConsentCatalogue, ConsentCatalogueAdmin)


class AttachedModelAdmin(BaseModelAdmin):
    list_display = ('content_type_map', 'consent_catalogue', 'is_active', 'created')
    list_filter = ('consent_catalogue', 'is_active', 'created')
    search_fields = ('content_type_map__model', 'content_type_map__app_label', 'content_type_map__name',)
admin.site.register(AttachedModel, AttachedModelAdmin)
