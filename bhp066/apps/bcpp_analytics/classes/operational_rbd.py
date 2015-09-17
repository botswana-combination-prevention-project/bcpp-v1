import collections
import datetime

from bhp066.apps.bcpp_clinic.models import (
    ClinicConsent, ClinicEligibility, ClinicRefusal, ClinicEnrollmentLoss,
    Questionnaire, ClinicVlResult, ViralLoadTracking)
from bhp066.apps.bcpp_lab.models import ClinicRequisition

from .base_operational_report import BaseOperationalReport


class OperationalRbd(BaseOperationalReport):

    def report_data(self):
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)

        approached_subjects = ClinicEligibility.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username)
        self.data_dict['1. Total number of approached subjects'] = approached_subjects.count()

        eligible_subjects = ClinicEligibility.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                             created__gte=self.date_from,
                                                             created__lte=self.date_to,
                                                             user_created__icontains=self.ra_username,
                                                             is_eligible=True)
        self.data_dict['1a. ELIGIBLE subjects'] = eligible_subjects.count()

        ineligible_subjects = ClinicEligibility.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               is_eligible=False)
        self.data_dict['1b. INELIGIBLE subjects'] = ineligible_subjects.count()

        ineligible_pos_subjects = ClinicEligibility.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                                   created__gte=self.date_from,
                                                                   created__lte=self.date_to,
                                                                   user_created__icontains=self.ra_username,
                                                                   is_eligible=False,
                                                                   hiv_status='POS')
        self.data_dict['1bi. INELIGIBLE POS subjects'] = ineligible_pos_subjects.count()

        total_clinic_consents = ClinicConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                             created__gte=self.date_from,
                                                             created__lte=self.date_to,
                                                             user_created__icontains=self.ra_username)
        self.data_dict['2. Total number of consented subjects'] = total_clinic_consents.count()

        enrollment_loss = ClinicEnrollmentLoss.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                              created__gte=self.date_from,
                                                              created__lte=self.date_to,
                                                              user_created__icontains=self.ra_username)
        self.data_dict['3. Total enrollment losses'] = enrollment_loss.count()

        refused_participants = ClinicRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                            created__gte=self.date_from,
                                                            created__lte=self.date_to,
                                                            user_created__icontains=self.ra_username)
        self.data_dict['4. Total participation refusals'] = refused_participants.count()

        consent = ClinicConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                               created__gte=self.date_from,
                                               created__lte=self.date_to,
                                               user_created__icontains=self.ra_username)

        enrolled_by_htc = consent.exclude(lab_identifier='', pims_identifier='')
        self.data_dict['5. Subjects with HTC identifier'] = enrolled_by_htc.count()

        with_pims_identifier = consent.exclude(lab_identifier='', htc_identifier='')
        self.data_dict['5a. Subjects with PIMS identifier'] = with_pims_identifier.count()

        with_k_identifier = consent.exclude(htc_identifier='', pims_identifier='')
        self.data_dict['5b. Subjects with K# identifier'] = with_k_identifier.count()

        enrolled_by_initiation = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                              created__gte=self.date_from,
                                                              created__lte=self.date_to,
                                                              user_created__icontains=self.ra_username,
                                                              registration_type='initiation')
        self.data_dict['5c. Subjects enrolled by INITIATION'] = enrolled_by_initiation.count()

        enrolled_by_ccc = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='ccc_scheduled')
        self.data_dict['5d. Subjects enrolled by CCC'] = enrolled_by_ccc.count()

        enrolled_by_masa_vl = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                           created__gte=self.date_from,
                                                           created__lte=self.date_to,
                                                           user_created__icontains=self.ra_username,
                                                           registration_type='masa_vl_scheduled')
        self.data_dict['5e. Subjects enrolled by MASA scheduled VL'] = enrolled_by_masa_vl.count()

        enrolled_by_other_non_vl = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                created__gte=self.date_from,
                                                                created__lte=self.date_to,
                                                                user_created__icontains=self.ra_username,
                                                                registration_type='OTHER')
        self.data_dict['5f. Subjects enrolled by Other NON VL'] = enrolled_by_other_non_vl.count()

        total_requisitions = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                              created__gte=self.date_from,
                                                              created__lte=self.date_to,
                                                              user_created__icontains=self.ra_username,)
        self.data_dict['6. Total Clinic Requisitions'] = total_requisitions.count()

        rbd_requisitions = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                            created__gte=self.date_from,
                                                            created__lte=self.date_to,
                                                            user_created__icontains=self.ra_username,
                                                            panel__name='Research Blood Draw',
                                                            is_drawn='yes')
        self.data_dict['6a. Clinic RBD\'s drawn'] = rbd_requisitions.count()

        viral_load_requisitions = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                   created__gte=self.date_from,
                                                                   created__lte=self.date_to,
                                                                   user_created__icontains=self.ra_username,
                                                                   panel__name='Clinic Viral Load',
                                                                   is_drawn='yes')
        self.data_dict['6b. Clinic VL\'s drawn @ BHP'] = viral_load_requisitions.count()

        viral_loads_tracking = ViralLoadTracking.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                created__gte=self.date_from,
                                                                created__lte=self.date_to,
                                                                user_created__icontains=self.ra_username,
                                                                is_drawn='yes')
        self.data_dict['6c. Clinic VL\'s drawn by request from GOVT'] = viral_loads_tracking.count()

        rbd_req_not_drawn = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                             created__gte=self.date_from,
                                                             created__lte=self.date_to,
                                                             user_created__icontains=self.ra_username,
                                                             panel__name='Research Blood Draw',
                                                             is_drawn='no')
        self.data_dict['6d. Clinic RBD\'s - NO blood drawn'] = rbd_req_not_drawn.count()

        vl_requisitions_not_drawn = ClinicRequisition.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                     created__gte=self.date_from,
                                                                     created__lte=self.date_to,
                                                                     user_created__icontains=self.ra_username,
                                                                     panel__name='Clinic Viral Load',
                                                                     is_drawn='no')
        self.data_dict['6e. Clinic VL\'s - NO blood drawn'] = vl_requisitions_not_drawn.count()

        vl_results_received = ClinicVlResult.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                            created__gte=self.date_from,
                                                            created__lte=self.date_to,
                                                            user_created__icontains=self.ra_username)
        self.data_dict['7. Clinic VL Results entered'] = vl_results_received.count()

        self.data_dict['8. Clinic VL Results MISSING from both GOVT & BHP'] = (viral_load_requisitions.count() + viral_loads_tracking.count()) - vl_results_received.count()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values
