from bhp_base_admin.admin import BaseTabularInline


class BaseConsentUpdateInlineAdmin(BaseTabularInline):
    extra = 0
    readonly_fields = ('consent_version', )
