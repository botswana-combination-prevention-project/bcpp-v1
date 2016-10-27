import collections
import datetime


from edc.entry_meta_data.models.scheduled_entry_meta_data import ScheduledEntryMetaData
from edc.subject.entry.models import Entry
from edc_constants.constants import NEW

from bhp066.apps.bcpp_clinic.models import (
    ClinicConsent, ClinicEligibility, ClinicRefusal, ClinicEnrollmentLoss,
    Questionnaire, ClinicVlResult, ViralLoadTracking)
from bhp066.apps.bcpp_lab.models import ClinicRequisition, SubjectRequisition

from .base_operational_report import BaseOperationalReport


class OperationalRbd(BaseOperationalReport):

    def report_data(self):
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)

        total_requisitions = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                              created__gte=self.date_from,
                                                              created__lte=self.date_to,
                                                              user_created__icontains=self.ra_username,)
        self.data_dict['a. Total Clinic Requisitions'] = total_requisitions.count()

        total_bhs_requisitions = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__household_structure__survey__survey_slug='bcpp-year-1',
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            panel__name='Research Blood Draw',)
        self.data_dict['b. Total BHS Subject Requisitions'] = total_bhs_requisitions.count()

        total_t1_requisitions = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__household_structure__survey__survey_slug='bcpp-year-2',
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            panel__name='Research Blood Draw',)
        self.data_dict['c. Total T1 Subject Requisitions'] = total_t1_requisitions.count()

        total_t2_requisitions = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            subject_visit__household_member__household_structure__survey__survey_slug='bcpp-year-3',
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            panel__name='Research Blood Draw',)
        self.data_dict['d. Total T2 Subject Requisitions'] = total_t2_requisitions.count()

        clinic_rbd = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                      created__gte=self.date_from,
                                                      created__lte=self.date_to,
                                                      user_created__icontains=self.ra_username,
                                                      panel__name='Research Blood Draw',
                                                      is_drawn='yes')
        self.data_dict['e. Clinic RBD\'s drawn'] = clinic_rbd.count()
        clinic_bhs_rbd = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__in=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            panel__name='Research Blood Draw',
            is_drawn='yes')
        self.data_dict['f. BHS CPC RBD\'s drawn'] = clinic_bhs_rbd.count()

        clinic_vl_requisitions = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                  created__gte=self.date_from,
                                                                  created__lte=self.date_to,
                                                                  user_created__icontains=self.ra_username,
                                                                  panel__name='Clinic Viral Load',
                                                                  is_drawn='yes')
        self.data_dict['g. Clinic VL\'s drawn @ BHP'] = clinic_vl_requisitions.count()
        clinic_bhs_vl = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community__in=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            panel__name='Viral Load',
            is_drawn='yes')
        self.data_dict['h. BHS CPC VL\'s drawn'] = clinic_bhs_vl.count()

        govt_vl_request = ViralLoadTracking.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                           created__gte=self.date_from,
                                                           created__lte=self.date_to,
                                                           user_created__icontains=self.ra_username,
                                                           is_drawn='yes')
        self.data_dict['i. Clinic VL\'s drawn by request from GOVT'] = govt_vl_request.count()

        rbd_not_drawn = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                         created__gte=self.date_from,
                                                         created__lte=self.date_to,
                                                         user_created__icontains=self.ra_username,
                                                         panel__name='Research Blood Draw',
                                                         is_drawn='no')
        self.data_dict['j. Clinic RBD\'s - NO blood drawn'] = rbd_not_drawn.count()

        vl_not_drawn = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                        created__gte=self.date_from,
                                                        created__lte=self.date_to,
                                                        user_created__icontains=self.ra_username,
                                                        panel__name='Clinic Viral Load',
                                                        is_drawn='no')
        self.data_dict['k. Clinic VL\'s - NO blood drawn'] = vl_not_drawn.count()

        vl_results_keyed = ClinicVlResult.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                         created__gte=self.date_from,
                                                         created__lte=self.date_to,
                                                         user_created__icontains=self.ra_username)
        self.data_dict['l. Clinic VL Results keyed'] = vl_results_keyed.count()

        unkeyed_vl_results = Entry.objects.filter(model_name='clinicvlresult', visit_definition__code='C0')
        for result_entries in unkeyed_vl_results:
            check_results_meta = ScheduledEntryMetaData.objects.filter(
                created__gte=self.date_from,
                created__lte=self.date_to,
                registered_subject__study_site__site_name__icontains=self.community,
                entry=result_entries,
                entry_status=NEW)
            self.data_dict['m. Consented subjects missing clinic VL results'] = check_results_meta.count()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values
