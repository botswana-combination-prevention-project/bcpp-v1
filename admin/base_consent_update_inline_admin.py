from bhp_base_model.classes import BaseTabularInline
#from bhp_consent.models import ConsentCatalogue


class BaseConsentUpdateInlineAdmin(BaseTabularInline):
    extra = 0
    readonly_fields = ('consent_version', )
