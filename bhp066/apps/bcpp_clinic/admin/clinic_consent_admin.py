from django.contrib import admin

from edc.subject.consent.admin import BaseConsentModelAdmin

from ..forms import ClinicConsentForm
from ..models import ClinicConsent


class ClinicConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'clinic'
    form = ClinicConsentForm

    def __init__(self, *args, **kwargs):
        super(ClinicConsentAdmin, self).__init__(*args, **kwargs)
        self.fields.remove('is_incarcerated')
        self.fields.extend(['lab_identifier', 'htc_identifier', 'pims_identifier'])
        self.list_filter.append('community')

admin.site.register(ClinicConsent, ClinicConsentAdmin)
