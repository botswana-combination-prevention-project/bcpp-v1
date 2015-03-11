import collections
import datetime
from django.db.models import Count
from django.contrib.auth.models import User
from edc.core.bhp_birt_reports.classes import OperationalReportUtilities
from edc.device.dispatch.models import DispatchContainerRegister

from apps.bcpp_household.constants import (CONFIRMED, UNCONFIRMED, INACCESSIBLE, NON_RESIDENTIAL,
                                           RESIDENTIAL_NOT_HABITABLE, RESIDENTIAL_HABITABLE)
from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_household.models import (Plot, PlotLogEntry, HouseholdStructure, Household, HouseholdAssessment)


class OperationalHousehold():

    def __init__(self, request):
        self.household_info = {}
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

    def return_household_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        household = Household.objects.all()
        self.household_info['1. Total Households'] = household.filter(plot__community__icontains=self.community,
                                               modified__gte=self.date_from, modified__lte=self.date_to,
                                               user_modified__icontains=self.ra_username).count()
        household_enumerated_structures = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=True)
        household_enumerated = household_enumerated_structures.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['2. Enumerated households'] = len(household_enumerated)
        #household_info['1. Plots reached'] = reached
        household_non_enumerated_structures = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=True)
        household_non_enumerated = household_non_enumerated_structures.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['3. Non enumerated households'] = len(household_non_enumerated)
        household_non_enumerated_hoh_absent = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=False)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=False,
                                                             failed_enumeration_attempts=1)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['6. Household failed enumeration attempt 1'] = len(failed_enumeration_attempts_structure)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=False,
                                                             failed_enumeration_attempts=2)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['7. Household failed enumeration attempt 2'] = len(failed_enumeration_attempts_structure)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=False,
                                                             failed_enumeration_attempts=3)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['8. Household failed enumeration attempt 3'] = len(failed_enumeration_attempts_structure)
        house_recidency_assesed = HouseholdAssessment.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username)
        house_recidency_assesed_uniques = house_recidency_assesed.values('household_structure__household__household_identifier').annotate(dcount=Count('household_structure__household__household_identifier'))
        self.household_info['9. Household Residency status assessed'] = len(house_recidency_assesed_uniques)
        enrolled_structure = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enrolled=True)
        enrolled = enrolled_structure.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['91. Enrolledenrolled households'] = len(enrolled)
        not_enrolled_structure = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enrolled=False)
        not_enrolled = not_enrolled_structure.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.household_info['92. Non enrolled households'] = len(not_enrolled)

        self.household_info['93. Non enrolled: no eligible members'] = len(enrolled)

        self.household_info['94. Non enrolled: All eligible refused'] = 0

        household_non_enumerated_absent = household_non_enumerated_hoh_absent.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        
        self.household_info['4. Non enumerated households: HOH Absent'] = 0#len(household_non_enumerated_absent)
        
        self.household_info['5. Non enumerated households: HOH Refused'] = 0#not_accessible_plots1
        
        self.household_info['96. Non enumerated: all eligible absent once'] = 0
        
        self.household_info['97. Non enumerated: all eligible absent twice'] = 0
        
        self.household_info['98. Non enumerated: all eligible absent thrice'] = 0
        
        self.household_info['99. Replaceable house holds'] = 0
        
        self.household_info['991. Replaced households'] = 0

        values = collections.OrderedDict(sorted(self.household_info.items()))
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