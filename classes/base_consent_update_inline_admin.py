from bhp_base_model.classes import BaseTabularInline
#from bhp_consent.models import ConsentCatalogue


class BaseConsentUpdateInlineAdmin(BaseTabularInline):
    extra = 0
    readonly_fields = ('consent_version', )

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "consent_catalogue":
#            kwargs["queryset"] = ConsentCatalogue.objects.filter(list_for_update=True)
#        super(BaseConsentUpdateInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
