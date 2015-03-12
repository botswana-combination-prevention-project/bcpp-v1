import collections
import datetime
from django.contrib.auth.models import User
from edc.core.bhp_birt_reports.classes import OperationalReportUtilities
from edc.constants import NO

from apps.bcpp_lab.models import SubjectRequisition
from apps.bcpp.choices import COMMUNITIES


class OperationalSpecimen():

    def __init__(self, request):
        self.specimen_info = {}
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

    def return_specimen_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        requisitions = SubjectRequisition.objects.filter(community__icontains=self.community,
                                                      modified__gte=self.date_from, modified__lte=self.date_to,
                                                      user_modified__icontains=self.ra_username)
        number_requisitions = requisitions.count()
        self.specimen_info['1. Total No. of requisitions'] = number_requisitions
        requisitions_received = requisitions.filter(is_receive=True).count()
        self.specimen_info['2. Total No. of requisitions received'] = requisitions_received
        microtube_requisitions = requisitions.filter(panel__name='Microtube').count()
        self.specimen_info['3. Total No. of microtube requisitions'] = microtube_requisitions
        failed_microtube = requisitions.filter(panel__name='Microtube', is_drawn=NO).count()
        self.specimen_info['4. Total No. of FAILED microtube requisitions'] = failed_microtube
        viral_load_requisitions = requisitions.filter(panel__name='Viral Load').count()
        self.specimen_info['5. Total No. of viral load requisitions'] = viral_load_requisitions
        rbd_requisitions = requisitions.filter(panel__name='Research Blood Draw').count()
        self.specimen_info['6. Total No. of research blood draw requisitions'] = rbd_requisitions
        venous_requisitions = requisitions.filter(panel__name='Venous (HIV)').count()
        self.specimen_info['7. Total No. of venous requisitions requisitions'] = venous_requisitions
        elisa_requisitions = requisitions.filter(panel__name='ELISA').count()
        self.specimen_info['8. Total No. of elisa requisitions requisitions'] = elisa_requisitions

        values = collections.OrderedDict(sorted(self.specimen_info.items()))
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