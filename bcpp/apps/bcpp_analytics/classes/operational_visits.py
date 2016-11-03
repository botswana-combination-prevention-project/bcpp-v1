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
        self.data_dict['1a. Unattended appointments (NEW)'] = new_visits.count()

        incomplete_visits = Appointment.objects.filter(
            study_site__site_name__icontains=self.community,
            modified__gte=self.date_from,
            modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            appt_status=INCOMPLETE,
            visit_definition__code='C0')
        self.data_dict['1b. INCOMPLETE appointments'] = incomplete_visits.count()

        inprogress_visits = Appointment.objects.filter(
            registered_subject__study_site__site_name__icontains=self.community,
            modified__gte=self.date_from,
            modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            appt_status=IN_PROGRESS,
            visit_definition__code='C0')
        self.data_dict['1c. IN_PROGRESS appointments'] = inprogress_visits.count()

        eligible_uconsented = ClinicEligibility.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            is_eligible=True,
            is_consented=False,
            is_refused=False)
        self.data_dict['2. Eligible but not yet consented'] = eligible_uconsented.count()

        dont_store_samples = ClinicConsent.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            may_store_samples=NO)
        self.data_dict['3. Consented but DO NOT STORE SAMPLES'] = dont_store_samples.count()

        unkeyed_locator = Entry.objects.filter(
            model_name='clinicsubjectlocator', visit_definition__code='C0')
        for entries in unkeyed_locator:
            locator_meta = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=entries,
                entry_status=NEW)
            self.data_dict['4. Consented subjects missing locator info'] = locator_meta.count()

        entry = Entry.objects.filter(model_name='questionnaire', visit_definition__code='C0')
        for entries in entry:
            question_meta = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=entries,
                entry_status=NEW)
            self.data_dict['5. Consented subjects with Questionnaire form unkeyed'] = question_meta.count()

        unkeyed_vl_tracking = Entry.objects.filter(model_name="viralloadtracking", visit_definition__code='C0')
        for entries in unkeyed_vl_tracking:
            vl_meta_data = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=entries,
                entry_status=NEW)
            self.data_dict['6. Consented subjects with GOVT VL Tracking form unkeyed'] = vl_meta_data.count()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values
