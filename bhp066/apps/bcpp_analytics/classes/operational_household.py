import collections
import datetime
from django.db.models import Count

from apps.bcpp_household.models import (HouseholdStructure, Household, HouseholdAssessment)

from .base_operational_report import BaseOperationalReport


class OperationalHousehold(BaseOperationalReport):

    def report_data(self):

        if self.community.find('----') != -1:
            self.community = ''
        if self.ra_username.find('----') != -1:
            self.ra_username = ''
        self.date_to += datetime.timedelta(days=1)
        household = Household.objects.all()
        self.data_dict['1. Total Households'] = household.filter(plot__community__icontains=self.community,
                                               modified__gte=self.date_from, modified__lte=self.date_to,
                                               user_modified__icontains=self.ra_username).count()
        household_enumerated_structures = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=True)
        household_enumerated = household_enumerated_structures.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['2. Enumerated households'] = len(household_enumerated)
        #data_dict['1. Plots reached'] = reached
        household_non_enumerated_structures = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=True)
        household_non_enumerated = household_non_enumerated_structures.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['3. Non enumerated households'] = len(household_non_enumerated)
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
        self.data_dict['6. Household failed enumeration attempt 1'] = len(failed_enumeration_attempts_structure)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=False,
                                                             failed_enumeration_attempts=2)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['7. Household failed enumeration attempt 2'] = len(failed_enumeration_attempts_structure)
        failed_enumeration_attempts = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enumerated=False,
                                                             failed_enumeration_attempts=3)
        failed_enumeration_attempts_structure = failed_enumeration_attempts.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['8. Household failed enumeration attempt 3'] = len(failed_enumeration_attempts_structure)
        house_recidency_assesed = HouseholdAssessment.objects.filter(household_structure__household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username)
        house_recidency_assesed_uniques = house_recidency_assesed.values('household_structure__household__household_identifier').annotate(dcount=Count('household_structure__household__household_identifier'))
        self.data_dict['9. Household Residency status assessed'] = len(house_recidency_assesed_uniques)
        enrolled_structure = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enrolled=True)
        enrolled = enrolled_structure.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['91. Enrolledenrolled households'] = len(enrolled)
        not_enrolled_structure = HouseholdStructure.objects.filter(household__plot__community__icontains=self.community,
                                                             modified__gte=self.date_from, modified__lte=self.date_to,
                                                             user_modified__icontains=self.ra_username,
                                                             enrolled=False)
        not_enrolled = not_enrolled_structure.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))
        self.data_dict['92. Non enrolled households'] = len(not_enrolled)

        self.data_dict['93. Non enrolled: no eligible members'] = len(enrolled)

        self.data_dict['94. Non enrolled: All eligible refused'] = 'N/A'

        household_non_enumerated_absent = household_non_enumerated_hoh_absent.values('household__household_identifier').annotate(dcount=Count('household__household_identifier'))

        self.data_dict['4. Non enumerated households: HOH Absent'] = 'N/A'#len(household_non_enumerated_absent)

        self.data_dict['5. Non enumerated households: HOH Refused'] = 'N/A'#not_accessible_plots1

        self.data_dict['96. Non enumerated: all eligible absent once'] = 'N/A'

        self.data_dict['97. Non enumerated: all eligible absent twice'] = 'N/A'

        self.data_dict['98. Non enumerated: all eligible absent thrice'] = 'N/A'

        self.data_dict['99. Replaceable house holds'] = 'N/A'

        self.data_dict['991. Replaced households'] = 'N/A'

        values = collections.OrderedDict(sorted(self.data_dict.items()))
        return values