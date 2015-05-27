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
        self.search_fields.append('first_name')
        self.search_fields.append('htc_identifier')
        self.search_fields.append('lab_identifier')
        self.search_fields.append('pims_identifier')
        self.list_display.insert(1, 'htc_identifier')
        self.list_display.insert(2, 'lab_identifier')
        self.list_display.insert(3, 'pims_identifier')

admin.site.register(ClinicConsent, ClinicConsentAdmin)
