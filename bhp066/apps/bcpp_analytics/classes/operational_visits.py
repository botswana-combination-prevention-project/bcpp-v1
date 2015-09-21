import collections
import datetime

from edc_constants.constants import DONE, INCOMPLETE, IN_PROGRESS, NO, NEW

from edc.entry_meta_data.models.scheduled_entry_meta_data import ScheduledEntryMetaData
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import Entry

from bhp066.apps.bcpp_clinic.models import ClinicConsent
from bhp066.apps.bcpp_clinic.models.clinic_eligibility import ClinicEligibility

from .base_operational_report import BaseOperationalReport


class OperationalVisits(BaseOperationalReport):

    def report_data(self):
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)

        all_app = Appointment.objects.filter(
            visit_definition__code='C0',
            registered_subject__study_site__site_name__icontains=self.community,)
        self.data_dict['1. All appointments'] = all_app.count()

        new_visits = Appointment.objects.filter(
            registered_subject__study_site__site_name__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            appt_status__icontains='new',
            visit_definition__code='C0')
        self.data_dict['1a. Visits not yet processed (NEW)'] = new_visits.count()

        completed_visits = Appointment.objects.filter(
            study_site__site_name__icontains=self.community,
            modified__gte=self.date_from,
            modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            appt_status=DONE,
            visit_definition__code='C0')
        self.data_dict['1b. Total number of COMPLETED visits'] = completed_visits.count()

        incomplete_visits = Appointment.objects.filter(
            study_site__site_name__icontains=self.community,
            modified__gte=self.date_from,
            modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            appt_status=INCOMPLETE,
            visit_definition__code='C0')
        self.data_dict['1c. Total number of INCOMPLETE visits'] = incomplete_visits.count()

        inprogress_visits = Appointment.objects.filter(
            registered_subject__study_site__site_name__icontains=self.community,
            modified__gte=self.date_from,
            modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            appt_status=IN_PROGRESS,
            visit_definition__code='C0')
        self.data_dict['1d. Total number of visits that are IN_PROGRESS'] = inprogress_visits.count()

        eligible_consent = ClinicEligibility.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            is_eligible=True,
            is_consented=False,
            is_refused=False)
        self.data_dict['2. Eligible but not yet consented'] = eligible_consent.count()

        no_samples = ClinicConsent.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            may_store_samples=NO)
        self.data_dict['3. Consented but DO NOT STORE SAMPLES'] = no_samples.count()

        locator_entry = Entry.objects.filter(model_name='clinicsubjectlocator', visit_definition__code='C0')
        for entries in locator_entry:
            locator_meta = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=entries,
                entry_status=NEW)
            self.data_dict['4. Consented subjects missing locator/ demographics info'] = locator_meta.count()

        entry = Entry.objects.filter(model_name='questionnaire', visit_definition__code='C0')
        for entries in entry:
            question_meta = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=entries,
                entry_status=NEW)
            self.data_dict['5. Consented subjects not under any registration status (e.g initiation, masa)'] = question_meta.count()

        vl_entry = Entry.objects.filter(model_name="viralloadtracking", visit_definition__code='C0')
        for entries in vl_entry:
            vl_meta_data = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=entries,
                entry_status=NEW)
            self.data_dict['6. Consented subjects with GOVT VL form available but not entered'] = vl_meta_data.count()

        vl_result_entry = Entry.objects.filter(model_name='clinicvlresult', visit_definition__code='C0')
        for result_entries in vl_result_entry:
            check_results_meta = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=result_entries,
                entry_status=NEW)
            self.data_dict['7. Consented subjects missing clinic VL results'] = check_results_meta.count()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values
