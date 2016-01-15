import collections
import datetime

from bhp066.apps.bcpp_clinic.models import (
    ClinicConsent, ClinicEligibility, ClinicRefusal, ClinicEnrollmentLoss,
    Questionnaire, ClinicVlResult, ViralLoadTracking)
from bhp066.apps.bcpp_lab.models import ClinicRequisition

from .base_operational_report import BaseOperationalReport


class OperationalConsents(BaseOperationalReport):

    def report_data(self):
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)

        eligible_subjects = ClinicEligibility.objects.filter(
            household_member__registered_subject__study_site__site_name__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            is_eligible=True,
            is_refused=False)
        self.data_dict['1. ELIGIBLE subjects'] = eligible_subjects.count()

        ineligible_subjects = ClinicEligibility.objects.filter(
            household_member__registered_subject__study_site__site_name__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            is_eligible=False,
            is_refused=False)
        self.data_dict['1a. INELIGIBLE subjects'] = ineligible_subjects.count()

        total_clinic_consents = ClinicConsent.objects.filter(
            household_member__registered_subject__study_site__site_name__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username)
        self.data_dict['2. Total number of consented subjects'] = total_clinic_consents.count()

        verified_clinic_consents = ClinicConsent.objects.filter(
            household_member__registered_subject__study_site__site_name__icontains=self.community,
            is_verified=True,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username)
        self.data_dict['2a. Total number of verified consents'] = verified_clinic_consents.count()

        enrolled_by_initiation = Questionnaire.objects.filter(
            clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            registration_type='initiation')
        self.data_dict['3. Subjects enrolled by INITIATION'] = enrolled_by_initiation.count()

        enrolled_by_ccc = Questionnaire.objects.filter(
            clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            registration_type='ccc_scheduled')
        self.data_dict['4. Subjects enrolled by CCC'] = enrolled_by_ccc.count()

        enrolled_by_masa_vl = Questionnaire.objects.filter(
            clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            registration_type='masa_vl_scheduled')
        self.data_dict['5. Subjects enrolled by MASA scheduled VL'] = enrolled_by_masa_vl.count()

        enrolled_by_other_non_vl = Questionnaire.objects.filter(
            clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username,
            registration_type='OTHER')
        self.data_dict['6. Subjects enrolled by Other NON VL'] = enrolled_by_other_non_vl.count()

        enrollment_loss = ClinicEnrollmentLoss.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username)
        self.data_dict['7. Total enrollment losses'] = enrollment_loss.count()

        refused_participants = ClinicRefusal.objects.filter(
            household_member__household_structure__household__plot__community__icontains=self.community,
            created__gte=self.date_from,
            created__lte=self.date_to,
            user_created__icontains=self.ra_username)
        self.data_dict['8. Total participation refusals'] = refused_participants.count()

#         consent = ClinicConsent.objects.filter(
#             household_member__registered_subject__study_site__site_name__icontains=self.community,
#             created__gte=self.date_from,
#             created__lte=self.date_to,
#             user_created__icontains=self.ra_username)
#
#         enrolled_by_htc = consent.exclude(lab_identifier='', pims_identifier='')
#         self.data_dict['5. Subject has HTC identifier'] = enrolled_by_htc.count()
#
#         with_pims_identifier = consent.exclude(lab_identifier='', htc_identifier='')
#         self.data_dict['5a. Subject has PIMS identifier'] = with_pims_identifier.count()
#
#         with_k_identifier = consent.exclude(htc_identifier='', pims_identifier='')
#         self.data_dict['5b. Subject has K# identifier'] = with_k_identifier.count()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values
