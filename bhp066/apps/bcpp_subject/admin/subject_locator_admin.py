from collections import OrderedDict

from django.contrib import admin

from edc.export.actions import export_as_csv_action

from ..filters import SubjectLocatorIsReferredListFilter, SubjectCommunityListFilter
from ..forms import SubjectLocatorForm
from ..models import SubjectLocator

from .subject_visit_model_admin import SubjectVisitModelAdmin


class SubjectLocatorAdmin(SubjectVisitModelAdmin):

    form = SubjectLocatorForm
    fields = (
        'subject_visit',
        'date_signed',
        'mail_address',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'may_sms_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'alt_contact_cell_number',
        'contact_phone',
        'has_alt_contact',
        'alt_contact_name',
        'alt_contact_rel',
        'alt_contact_cell',
        'other_alt_contact_cell',
        'alt_contact_tel',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',)
    radio_fields = {
        "home_visit_permission": admin.VERTICAL,
        "may_follow_up": admin.VERTICAL,
        "may_sms_follow_up": admin.VERTICAL,
        "has_alt_contact": admin.VERTICAL,
        "may_call_work": admin.VERTICAL,
        "may_contact_someone": admin.VERTICAL, }
    list_filter = (SubjectLocatorIsReferredListFilter, SubjectCommunityListFilter, 'may_follow_up', 'may_contact_someone', 'may_call_work', "home_visit_permission")
    list_display = ('subject_visit', 'date_signed', "home_visit_permission", "may_follow_up", "may_sms_follow_up", "has_alt_contact", "may_call_work", "may_contact_someone")

    def get_actions(self, request):
        actions = super(SubjectLocatorAdmin, self).get_actions(request)
        actions['export_as_pipe_action'] = (  # This is a django SortedDict (function, name, short_description)
            export_as_csv_action(
                delimiter='|',
                encrypt=False,
                exclude=['id', 'exported', 'exported_datetime', self.visit_model_foreign_key, 'revision', 'hostname_created', 'hostname_modified', 'created', 'modified', 'user_created', 'user_modified', 'comment'],
                extra_fields=OrderedDict(
                    {'subject_identifier': self.visit_model_foreign_key + '__appointment__registered_subject__subject_identifier',
                     'first_name': self.visit_model_foreign_key + '__appointment__registered_subject__first_name',
                     'last_name': self.visit_model_foreign_key + '__appointment__registered_subject__last_name',
                     'initials': self.visit_model_foreign_key + '__appointment__registered_subject__initials',
                     'dob': self.visit_model_foreign_key + '__appointment__registered_subject__dob',
                     'identity': self.visit_model_foreign_key + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_model_foreign_key + '__appointment__registered_subject__identity_type',
                     })
                ),
                'export_as_pipe_action',
                "Export Locator to Pipe delimited file")
        return actions

admin.site.register(SubjectLocator, SubjectLocatorAdmin)
