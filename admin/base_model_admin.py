from bhp_base_admin.mixin import SiteMixin
from bhp_site_edc import edc as admin


class BaseModelAdmin (SiteMixin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)
