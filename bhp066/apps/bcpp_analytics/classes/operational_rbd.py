import collections
import datetime

from apps.bcpp_clinic.models import (ClinicConsent, ClinicEligibility, ClinicRefusal, ClinicEnrollmentLoss,
                                     Questionnaire)
from apps.bcpp_lab.models import SubjectRequisition

from .base_operational_report import BaseOperationalReport


class OperationalRbd(BaseOperationalReport):

    def report_data(self):
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        self.data_dict['1. 16-64 years old HIV+ community residents on ART in the community clinic'] = 'N/A'
        self.data_dict['2. 16-64 years old HIV+ community residents NOT on ART in the community clinic'] = 'N/A'
        referral_from_htc = ClinicConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                         created__gte=self.date_from,
                                                         created__lte=self.date_to,
                                                         user_created__icontains=self.ra_username).exclude(htc_identifier=None)
        self.data_dict['3. Referral from HTC campaign'] = referral_from_htc.count()
        potentials_approached = ClinicEligibility.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                                 created__gte=self.date_from,
                                                                 created__lte=self.date_to,
                                                                 user_created__icontains=self.ra_username)
        self.data_dict['4. Potential participants individually approached'] = potentials_approached.count()
        enrolled_participants = ClinicConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                         created__gte=self.date_from,
                                                         created__lte=self.date_to,
                                                         user_created__icontains=self.ra_username)
        self.data_dict['5. Participants that enrolled'] = enrolled_participants.count()
        refused_participants = ClinicRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                            created__gte=self.date_from,
                                                            created__lte=self.date_to,
                                                            user_created__icontains=self.ra_username)
        self.data_dict['6. Participants that refused'] = refused_participants.count()
        enrollment_loss = ClinicEnrollmentLoss.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                              created__gte=self.date_from,
                                                              created__lte=self.date_to,
                                                              user_created__icontains=self.ra_username)
        self.data_dict['6. Enrollment loss'] = enrollment_loss.count()
        enrolled_initiation = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='initiation')
        self.data_dict['6. Enrolled by initiation visit'] = enrolled_initiation.count()
        enrolled_ccc = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='ccc_scheduled')
        self.data_dict['6. Enrolled by ccc'] = enrolled_ccc.count()
        enrolled_scheduled = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='masa_vl_scheduled')
        self.data_dict['6. Enrolled by scheduled viral load visit'] = enrolled_scheduled.count()
        enrolled_non_viral_load = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               registration_type='OTHER')
        self.data_dict['6. Enrolled by non viral load visit'] = enrolled_non_viral_load.count()
        viral_load_requisitions = SubjectRequisition.objects.filter(community__icontains=self.community,
                                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                                      user_modified__icontains=self.ra_username,
                                                      panel__name='Viral Load')
        self.data_dict['6. Viral load requisitions'] = viral_load_requisitions.count()
        self.data_dict['6. Viral load results received'] = 'N/A'
        self.data_dict['6. Viral load results pending'] = 'N/A'

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values