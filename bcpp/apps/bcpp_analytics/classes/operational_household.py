import collections
import datetime
import threading
from django.db.models import Count

from bhp066.apps.bcpp_household.models import (HouseholdStructure, Household, HouseholdAssessment, HouseholdLogEntry)
from bhp066.apps.bcpp_household.helpers import ReplacementHelper
from bhp066.apps.bcpp_household.constants import REFUSED_ENUMERATION, ELIGIBLE_REPRESENTATIVE_ABSENT

from .base_operational_report import BaseOperationalReport


class OperationalHousehold(BaseOperationalReport):

    def report_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        threads = []
        household = Household.objects.filter(
            plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username)
        self.data_dict['1. Total Households'] = household.count()
        household_enumerated_structures = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            enumerated=True)
        household_enumerated = household_enumerated_structures.values(
            'household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['2. Enumerated households'] = len(household_enumerated)

        household_non_enumerated_structures = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            enumerated=False).exclude(survey__survey_slug='bcpp-year-3')
        household_non_enumerated = household_non_enumerated_structures.values(
            'household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['3. Non enumerated households'] = len(household_non_enumerated)
        # Create new threads
        thread1 = NonEnumeratedHouseholds(
            1, "NonEnumeratedHouseholds-1", 1, household_non_enumerated_structures, self.data_dict)
        thread1.start()
        not_enrolled_structure = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username).exclude(enrolled=True).exclude(survey__survey_slug='bcpp-year-3')
        not_enrolled = not_enrolled_structure.values('household__household_identifier').annotate(
            dcount=Count('household__household_identifier'))
        self.data_dict['92. Non enrolled households'] = len(not_enrolled)
        thread2 = NonEnrolledHouseholds(1, "NonEnrolledHouseholds-1", 1, not_enrolled_structure, self.data_dict)
        thread2.start()
        threads.append(thread1)
        threads.append(thread2)
#         household_non_enumerated_hoh_absent = []
#         household_non_enumerated_hoh_refused = []
#         for hst in household_non_enumerated_structures:
#             log_entry = HouseholdLogEntry.objects.filter(household_log__household_structure=hst).order_by('-created')
#             if log_entry.exists() and (log_entry[0].household_status == REFUSED_ENUMERATION):
#                 household_non_enumerated_hoh_refused.append(hst)
#             elif log_entry.exists() and (log_entry[0].household_status == ELIGIBLE_REPRESENTATIVE_ABSENT):
#                 household_non_enumerated_hoh_absent.append(hst)
#             else:
#                 pass
        failed_enumeration_attempts = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            enumerated=False,
            failed_enumeration_attempts=1)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values(
            'household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['6. Household failed enumeration attempt 1'] = len(failed_enumeration_attempts_structure)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            enumerated=False,
            failed_enumeration_attempts=2)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values(
            'household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['7. Household failed enumeration attempt 2'] = len(failed_enumeration_attempts_structure)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            enumerated=False,
            failed_enumeration_attempts=3)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values(
            'household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['8. Household failed enumeration attempt 3'] = len(failed_enumeration_attempts_structure)
        house_recidency_assesed = HouseholdAssessment.objects.filter(
            household_structure__household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username)
        house_recidency_assesed_uniques = house_recidency_assesed.values(
            'household_structure__household__household_identifier').annotate(
                dcount=Count('household_structure__household__household_identifier'))
        self.data_dict['9. Household Residency status assessed'] = len(house_recidency_assesed_uniques)
        enrolled_structure = HouseholdStructure.objects.filter(
            household__plot__community__icontains=self.community,
            modified__gte=self.date_from, modified__lte=self.date_to,
            user_modified__icontains=self.ra_username,
            enrolled=True)
        enrolled = enrolled_structure.values('household__household_identifier').annotate(
            dcount=Count('household__household_identifier'))
        self.data_dict['91. Enrolled households'] = len(enrolled)

#         household_non_enrolled_no_eligible = []
#         household_non_enrolled_eligible_refused = []
#         for hst in not_enrolled_structure:
#             replacement_helper = ReplacementHelper(household_structure=hst)
#             if replacement_helper.all_eligible_members_refused:
#                 household_non_enrolled_eligible_refused.append(hst)
#             elif replacement_helper.all_eligible_members_absent:
#                 household_non_enrolled_no_eligible.append(hst)
#             else:
#                 pass
#         self.data_dict['93. Non enrolled: no eligible members'] = len(household_non_enrolled_no_eligible)
#
#         self.data_dict['94. Non enrolled: all eligible refused'] = len(household_non_enrolled_eligible_refused)

        self.data_dict['96. Non enumerated: all eligible absent once'] = 'N/A'

        self.data_dict['97. Non enumerated: all eligible absent twice'] = 'N/A'

        self.data_dict['98. Non enumerated: all eligible absent thrice'] = 'N/A'

        replaceable_households = Household.objects.filter(plot__community__icontains=self.community,
                                                          modified__gte=self.date_from, modified__lte=self.date_to,
                                                          user_modified__icontains=self.ra_username,
                                                          replaceable=True)

        self.data_dict['99. Replaceable households'] = replaceable_households.count()

        non_replaced_households = household.filter(replaced_by=None)

        self.data_dict['991. Replaced households'] = household.count() - non_replaced_households.count()

        # Wait for all threads to complete
        for t in threads:
            if t.is_alive():
                t.join()

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values


class NonEnumeratedHouseholds(threading.Thread):

    def __init__(self, thread_id, name, counter, household_non_enumerated_structures, data_dict):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter
        self.data_dict = data_dict
        self.household_non_enumerated_structures = household_non_enumerated_structures

    def run(self):
        print "Starting " + self.name
        household_non_enumerated_hoh_absent = []
        household_non_enumerated_hoh_refused = []
        for hst in self.household_non_enumerated_structures:
            log_entry = HouseholdLogEntry.objects.filter(household_log__household_structure=hst).order_by('-created')
            if log_entry.exists() and (log_entry[0].household_status == REFUSED_ENUMERATION):
                household_non_enumerated_hoh_refused.append(hst)
            elif log_entry.exists() and (log_entry[0].household_status == ELIGIBLE_REPRESENTATIVE_ABSENT):
                household_non_enumerated_hoh_absent.append(hst)
            else:
                pass
        self.data_dict['4. Non enumerated households: HOH Absent'] = len(household_non_enumerated_hoh_absent)
        self.data_dict['5. Non enumerated households: HOH Refused'] = len(household_non_enumerated_hoh_refused)


class NonEnrolledHouseholds(threading.Thread):

    def __init__(self, thread_id, name, counter, not_enrolled_structure, data_dict):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter
        self.data_dict = data_dict
        self.not_enrolled_structure = not_enrolled_structure

    def run(self):
        print "Starting " + self.name
        household_non_enrolled_no_eligible = []
        household_non_enrolled_eligible_refused = []
        for hst in self.not_enrolled_structure:
            replacement_helper = ReplacementHelper(household_structure=hst)
            if replacement_helper.all_eligible_members_refused:
                household_non_enrolled_eligible_refused.append(hst)
            elif replacement_helper.all_eligible_members_absent:
                household_non_enrolled_no_eligible.append(hst)
            else:
                pass
        self.data_dict['93. Non enrolled: no eligible members'] = len(household_non_enrolled_no_eligible)
        self.data_dict['94. Non enrolled: all eligible refused'] = len(household_non_enrolled_eligible_refused)
