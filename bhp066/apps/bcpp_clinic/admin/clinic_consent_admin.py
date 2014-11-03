from django.contrib import admin

from edc.subject.consent.admin import BaseConsentModelAdmin

from ..forms import ClinicConsentForm
from ..models import ClinicConsent


class ClinicConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'clinic'
    form = ClinicConsentForm

    def __init__(self, *args, **kwargs):
        super(ClinicConsentAdmin, self).__init__(*args, **kwargs)
        for fld in ['is_incarcerated']:
            self.fields.remove(fld)
        for flds in ['have_htc_pims', 'htc_pims_id']:
            self.fields.append(flds)

admin.site.register(ClinicConsent, ClinicConsentAdmin)
