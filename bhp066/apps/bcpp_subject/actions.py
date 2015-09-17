from datetime import datetime

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib import messages

from bhp066.config.celery import already_running, CeleryTaskAlreadyRunning, CeleryNotRunning

from edc.export.classes import ExportAsCsv

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.exceptions import SurveyValueError

from .choices import REFERRAL_CODES
from .models import SubjectReferral, CallLog, SubjectLocator
from .utils import update_referrals_for_hic, update_call_list, add_to_call_list


def update_call_list_action(modeladmin, request, queryset):
    update_call_list()
update_call_list_action.short_description = "Update Call List"


def add_to_call_list_action(modeladmin, request, queryset):
    for qs in queryset:
        add_to_call_list(qs)
add_to_call_list_action.short_description = "Add to Call List"


def call_participant(modeladmin, request, queryset):
    """Redirects to a new or existing CallLog.

    If required, creates enumeration data for the current survey
    """
    call_list = queryset[0]
    source_household_member = call_list.household_member
    household = source_household_member.household_structure.household
    source_survey = source_household_member.household_structure.survey
    target_survey = Survey.objects.current_survey()
    try:
        HouseholdStructure.objects.add_household_members_from_survey(
            household, source_survey, target_survey)
    except SurveyValueError:
        pass
    household_structure = HouseholdStructure.objects.get(
        household=household,
        survey=target_survey)
    household_member = HouseholdMember.objects.get(
        household_structure=household_structure,
        internal_identifier=source_household_member.internal_identifier)
    try:
        call_log = CallLog.objects.get(household_member=household_member)
        call_log.save()
    except CallLog.DoesNotExist:
        call_log = CallLog.objects.create(
            household_member=household_member,
            survey=Survey.objects.current_survey(datetime.today()),
            label=call_list.label,
            locator_information=SubjectLocator.objects.previous(household_member).formatted_locator_information
            )
    change_url = ('{}?household_member={}&next={}&q={}').format(
        reverse("admin:bcpp_subject_calllog_change", args=(call_log.pk, )),
        call_log.household_member.pk,
        "admin:{}_{}_changelist".format(call_list._meta.app_label, call_list._meta.object_name.lower()),
        request.GET.get('q'),)
    return HttpResponseRedirect(change_url)
call_participant.short_description = "Call participant"


def update_referrals(modeladmin, request, queryset):
    for obj in queryset:
        try:
            bhs_referral_code = SubjectReferral.objects.get(subject_visit=obj.subject_visit).referral_code
            obj.bhs_referral_code = bhs_referral_code
            obj.save(update_fields=['bhs_referral_code'])
        except SubjectReferral.DoesNotExist:
            pass
update_referrals.short_description = "Update selected referrals"


def update_referrals_for_hic_action(modeladmin, request, queryset, **kwargs):
    try:
        already_running(update_referrals_for_hic)
        result = update_referrals_for_hic.delay()
        messages.add_message(request, messages.INFO, (
            '{0.status}: Updating referrals for hic ({0.id})').format(result))
    except CeleryTaskAlreadyRunning as celery_task_already_running:
        messages.add_message(request, messages.WARNING, str(celery_task_already_running))
    except CeleryNotRunning as not_running:
        messages.add_message(request, messages.WARNING, str(not_running))
    except Exception as e:
        messages.add_message(request, messages.ERROR, (
            'Unable to run task. Celery got {}.'.format(str(e))))
update_referrals_for_hic_action.short_description = (
    'Update ALL referrals for HIC enrollments (runs in background).')


def export_referrals_for_cdc_action(description="Export Referrals for CDC (Manual)", fields=None, exclude=None,
                                    extra_fields=None, header=True, track_history=True, show_all_fields=True,
                                    delimiter=None, encrypt=True, strip=False):
    """Filters then exports a queryset from admin.

    The post admin filtering takes out:
      * out any referrals with an invalid or blank code.
      * any referrals NOT covered by an appointment that is DONE (appt_status=DONE).
      * any referrals that were previously exported (exported=True).

    """
    def export(modeladmin, request, queryset):
        referral_code_list = [key for key, value in REFERRAL_CODES if not key == 'pending']
        queryset = queryset.filter(
            referral_code__in=referral_code_list, in_clinic_flag=False)
        export_as_csv = ExportAsCsv(
            queryset,
            modeladmin=modeladmin,
            fields=fields,
            exclude=exclude,
            extra_fields=extra_fields,
            header=header,
            track_history=track_history,
            show_all_fields=show_all_fields,
            delimiter=delimiter,
            export_datetime=datetime.now(),
            encrypt=encrypt,
            strip=strip)
        return export_as_csv.write_to_file()

    export.short_description = description

    return export


def export_locator_for_cdc_action(description="Export Locator for CDC (Manual)",
                                  fields=None, exclude=None, extra_fields=None,
                                  header=True, track_history=True, show_all_fields=True,
                                  delimiter=None, encrypt=True, strip=False):

    def export(modeladmin, request, queryset):
        """Filter locator for those referred and data not yet seen in clinic (in_clinic_flag=False)."""
        referral_code_list = [key for key, value in REFERRAL_CODES if not key == 'pending']
        referred_subject_identifiers = [dct.get('subject_visit__subject_identifier')
                                        for dct in SubjectReferral.objects.values(
                                            'subject_visit__subject_identifier').filter(
                                                referral_code__in=referral_code_list, in_clinic_flag=False)]
        queryset = queryset.filter(subject_visit__subject_identifier__in=referred_subject_identifiers)
        export_as_csv = ExportAsCsv(
            queryset,
            modeladmin=modeladmin,
            fields=fields,
            exclude=exclude,
            extra_fields=extra_fields,
            header=header,
            track_history=track_history,
            show_all_fields=show_all_fields,
            delimiter=delimiter,
            export_datetime=datetime.now(),
            encrypt=encrypt,
            strip=strip)
        return export_as_csv.write_to_file()

    export.short_description = description

    return export
