from edc.export.classes import ExportAsCsv
from apps.bcpp_subject.choices import REFERRAL_CODES

from .models import SubjectReferral


def export_referrals_for_cdc_action(description="Export Referrals for CDC (Manual)",
                         fields=None, exclude=None, extra_fields=None, header=True, track_history=True, show_all_fields=True, delimiter=None, encrypt=True, strip=False):

    def export(modeladmin, request, queryset):
        referral_code_list = [key for key, value in REFERRAL_CODES if not key == 'pending']
        queryset = queryset.filter(referral_code__in=referral_code_list, in_clinic_flag=False)
        export_as_csv = ExportAsCsv(queryset,
                               modeladmin=modeladmin,
                               fields=fields,
                               exclude=exclude,
                               extra_fields=extra_fields,
                               header=header,
                               track_history=track_history,
                               show_all_fields=show_all_fields,
                               delimiter=delimiter,
                               encrypt=encrypt,
                               strip=strip)
        return export_as_csv.write_to_file()

    export.short_description = description

    return export


def export_locator_for_cdc_action(description="Export Locator for CDC (Manual)",
                                  fields=None, exclude=None, extra_fields=None, header=True, track_history=True, show_all_fields=True, delimiter=None, encrypt=True, strip=False):

    def export(modeladmin, request, queryset):
        """Filter locator for those referred and data not yet seen in clinic (in_clinic_flag=False)."""
        referral_code_list = [key for key, value in REFERRAL_CODES if not key == 'pending']
        referred_subject_identifiers = [dct.get('subject_visit__subject_identifier') for dct in SubjectReferral.objects.values('subject_visit__subject_identifier').filter(referral_code__in=referral_code_list, in_clinic_flag=False)]
        queryset = queryset.filter(subject_visit__subject_identifier__in=referred_subject_identifiers)
        export_as_csv = ExportAsCsv(queryset,
                               modeladmin=modeladmin,
                               fields=fields,
                               exclude=exclude,
                               extra_fields=extra_fields,
                               header=header,
                               track_history=track_history,
                               show_all_fields=show_all_fields,
                               delimiter=delimiter,
                               encrypt=encrypt,
                               strip=strip)
        return export_as_csv.write_to_file()

    export.short_description = description

    return export
