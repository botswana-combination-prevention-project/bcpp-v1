import collections
import datetime
from django.db.models import Count
from django.contrib.auth.models import User
from edc.core.bhp_birt_reports.classes import OperationalReportUtilities

from apps.bcpp_clinic.models import (ClinicConsent, ClinicEligibility, ClinicRefusal, ClinicEnrollmentLoss,
                                     Questionnaire)
from apps.bcpp_lab.models import SubjectRequisition
from apps.bcpp.choices import COMMUNITIES


class OperationalRbd():

    def __init__(self, request):
        self.rbd_info = {}
        self.utilities = OperationalReportUtilities()
        self.date_from = self.utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
        self.date_to = self.utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')
        self.ra_username = request.GET.get('ra', '')
        self.community = request.GET.get('community', '')
        self.previous_ra = self.ra_username
        self.previous_community = self.community
        self.communities = None
        self.ra_usernames = None

#     def operational_plots(self):
#         pass

    def return_communities(self):
        return self.communities

    def return_ra_usernames(self):
        return self.ra_usernames

    def return_rbd_data(self):
        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        self.rbd_info['1. 16-64 years old HIV+ community residents on ART in the community clinic'] = 'N/A'
        self.rbd_info['2. 16-64 years old HIV+ community residents NOT on ART in the community clinic'] = 'N/A'
        referral_from_htc = ClinicConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                         created__gte=self.date_from,
                                                         created__lte=self.date_to,
                                                         user_created__icontains=self.ra_username).exclude(htc_identifier=None)
        self.rbd_info['3. Referral from HTC campaign'] = referral_from_htc.count()
        potentials_approached = ClinicEligibility.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                                 created__gte=self.date_from,
                                                                 created__lte=self.date_to,
                                                                 user_created__icontains=self.ra_username)
        self.rbd_info['4. Potential participants individually approached'] = potentials_approached.count()
        enrolled_participants = ClinicConsent.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                         created__gte=self.date_from,
                                                         created__lte=self.date_to,
                                                         user_created__icontains=self.ra_username)
        self.rbd_info['5. Participants that enrolled'] = enrolled_participants.count()
        refused_participants = ClinicRefusal.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                            created__gte=self.date_from,
                                                            created__lte=self.date_to,
                                                            user_created__icontains=self.ra_username)
        self.rbd_info['6. Participants that refused'] = refused_participants.count()
        enrollment_loss = ClinicEnrollmentLoss.objects.filter(household_member__household_structure__household__plot__community__icontains=self.community,
                                                              created__gte=self.date_from,
                                                              created__lte=self.date_to,
                                                              user_created__icontains=self.ra_username)
        self.rbd_info['6. Enrollment loss'] = enrollment_loss.count()
        enrolled_initiation = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='initiation')
        self.rbd_info['6. Enrolled by initiation visit'] = enrolled_initiation.count()
        enrolled_ccc = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='ccc_scheduled')
        self.rbd_info['6. Enrolled by ccc'] = enrolled_ccc.count()
        enrolled_scheduled = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                       created__gte=self.date_from,
                                                       created__lte=self.date_to,
                                                       user_created__icontains=self.ra_username,
                                                       registration_type='masa_vl_scheduled')
        self.rbd_info['6. Enrolled by scheduled viral load visit'] = enrolled_scheduled.count()
        enrolled_non_viral_load = Questionnaire.objects.filter(clinic_visit__household_member__household_structure__household__plot__community__icontains=self.community,
                                                               created__gte=self.date_from,
                                                               created__lte=self.date_to,
                                                               user_created__icontains=self.ra_username,
                                                               registration_type='OTHER')
        self.rbd_info['6. Enrolled by non viral load visit'] = enrolled_non_viral_load.count()
        viral_load_requisitions = SubjectRequisition.objects.filter(community__icontains=self.community,
                                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                                      user_modified__icontains=self.ra_username,
                                                      panel__name='Viral Load')
        self.rbd_info['6. Viral load requisitions'] = viral_load_requisitions.count()
        self.rbd_info['6. Viral load results received'] = 'N/A'
        self.rbd_info['6. Viral load results pending'] = 'N/A'

        values = collections.OrderedDict(sorted(self.rbd_info.items()))
        communities = []
        if (self.previous_community.find('----') == -1) and (not self.previous_community == ''):  # Passing filtered results
            # communities = [community[0].lower() for community in  COMMUNITIES]
            for community in  COMMUNITIES:
                if community[0].lower() != self.previous_community:
                    communities.append(community[0])
            communities.insert(0, self.previous_community)
            communities.insert(1, '---------')
        else:
            communities = [community[0].lower() for community in  COMMUNITIES]
            communities.insert(0, '---------')
        self.communities = communities
        ra_usernames = []
        if (self.previous_ra.find('----') == -1) and (not self.previous_ra == ''):
            for ra_name in [user.username for user in User.objects.filter(groups__name='field_research_assistant')]:
                if ra_name != self.previous_ra:
                    ra_usernames.append(ra_name)
            ra_usernames.insert(0, self.previous_ra)
            ra_usernames.insert(1, '---------')
        else:
            ra_usernames = [user.username for user in User.objects.filter(groups__name='field_research_assistant')]
            ra_usernames.insert(0, '---------')
        self.ra_usernames = ra_usernames
        return values