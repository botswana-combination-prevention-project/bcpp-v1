import collections
import datetime

from apps.bcpp_clinic.models import (ClinicConsent, ClinicEligibility, ClinicRefusal, ClinicEnrollmentLoss,
                                     Questionnaire, ClinicVlResult, ViralLoadTracking)
from apps.bcpp_lab.models import ClinicRequisition

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
        self.data_dict['7. Enrollment loss'] = enrollment_loss.count()
        enrolled_initiation = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='initiation')
        self.data_dict['8. Enrolled by initiation visit'] = enrolled_initiation.count()
        enrolled_etc = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='etc_scheduled')
        self.data_dict['9. Enrolled by etc'] = enrolled_etc.count()
        enrolled_scheduled = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='masa_vl_scheduled')
        self.data_dict['91. Enrolled by scheduled viral load visit'] = enrolled_scheduled.count()
        enrolled_non_viral_load = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               registration_type='OTHER')
        self.data_dict['92. Enrolled by non viral load visit'] = enrolled_non_viral_load.count()
        rdb_requisitions = ClinicRequisition.objects.filter(community__icontains=self.community,
                                                            modified__gte=self.date_from, modified__lte=self.date_to,
                                                            user_modified__icontains=self.ra_username,
                                                            panel__name='Research Blood Draw',
                                                            is_drawn='Yes')
        self.data_dict['93. Research blood draw requisitions drawn'] = rdb_requisitions.count()
        viral_load_requisitions = ClinicRequisition.objects.filter(community__icontains=self.community,
                                                                    modified__gte=self.date_from, modified__lte=self.date_to,
                                                                    user_modified__icontains=self.ra_username,
                                                                    panel__name='Clinic Viral Load',
                                                                    is_drawn='Yes')
        self.data_dict['94. Viral load requisitions drawn for BHP'] = viral_load_requisitions.count()
        viral_loads_tracking = ViralLoadTracking.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                created__gte=self.date_from,
                                                                created__lte=self.date_to,
                                                                user_created__icontains=self.ra_username,
                                                                is_drawn='Yes')
        self.data_dict['95. Viral loads drawn on request of the government (viral load tracking form)'] = viral_loads_tracking.count()
        viral_loads_received = ClinicVlResult.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                                created__gte=self.date_from,
                                                                created__lte=self.date_to,
                                                                user_created__icontains=self.ra_username)
        self.data_dict['96. Viral load results received'] = viral_loads_received.count()
        self.data_dict['97. Viral load results pending'] = (viral_load_requisitions.count() + viral_loads_tracking.count()) - viral_loads_received.count()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values