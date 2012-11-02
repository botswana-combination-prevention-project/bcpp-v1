import re
from django.db.models import Q
from django.conf import settings
from lab_flag.classes import Flag
from django.db.models import get_model 
from lab_reference.classes import ReferenceFlag
import pdb


class GradeFlag(Flag):

    def check_list_prep(self, list_items):
        """Runs additional checks for the reference table.

        Ensures list not greater than 4.

        Confirms that only 4 instances of list_item are returned (G1,2,3,4) from :func:`get_list_prep`
        and that all 4 grades are represented.
        """
        grades = []
        for list_item in list_items:
            grades.append(list_item.grade)
        if len(grades) > 4:
            #for list_item in list_items:
            #    print '{0} {1} {2} {3}'.format(list_item.grade, list_item.age_low_days(), list_item.age_high_days(), list_item.hiv_status)
            raise TypeError('Duplicate instances for grade in reference list for test code {0} gender '
                            '{1} hiv status {2}. Got {3}.'.format(self.test_code, self.gender, self.hiv_status, grades))
        grades = list(set(grades))
        grades.sort()
        if grades != [1, 2, 3, 4]:
            raise TypeError('Missing ranges for grade in reference list for test code {0} gender {1} '
                            'hiv status {2}. Got ranges for "{3}".'.format(self.test_code, self.gender, self.hiv_status, grades))

    def get_lab_tracker_group_name(self):
        """Returns a group name to use when filtering on values in the lab_tracker class.

        See :mode:bhp_lab_tracker"""
        return 'HIV'

    def get_list_prep(self, test_code, gender, hiv_status, age_in_days):
        """Returns list of GradingListItems filtered on test_code, gender, hiv_status, age_in_days.

        .. note:: If ranges overlap after rounding, the higher grade should be selected
                  for the calculation. see :func:`order_list_prep`.
        """
        if hiv_status:
            qset = (Q(hiv_status__iexact=hiv_status.lower()) | Q(hiv_status__iexact='ANY'))
        else:
            qset = (Q(hiv_status__iexact='ANY'))
        list_items = self.list_item_model_cls.objects.filter(
            qset,
            **{'{0}__name__iexact'.format(self.list_name): settings.GRADING_LIST,
               'grading_list__name__iexact': settings.GRADING_LIST,
               'test_code': test_code,
               'gender__icontains': gender,
               'active': True})
        # return a filtered list of list_item instances
        return self.filter_list_items_by_age(list_items, self.age_in_days)

    def order_list_prep(self, list_items):
        """Returns an ordered list of list_items"""
        ordered_list_items = [None, None, None, None]
        if len(list_items) != 4:
            raise TypeError('Expected 4 grading list items. Got {0} from {1}.'.format(len(list_items), list_items))
        for list_item in list_items:
            ordered_list_items[4 - list_item.grade] = list_item
        return ordered_list_items

    def get_evaluate_prep(self, value, list_item):
        """ Determines if the value falls within one of the graded ranges."""
        eval_str = '{val} {value_low_quantifier} {lower_limit} and {val} {value_high_quantifier} {upper_limit}'
        flag = None
        #Ignore a record marked as dummy and return a None flag
        if list_item.dummy:
            lower_limit = list_item.value_low
            upper_limit = list_item.value_high
            return flag, lower_limit, upper_limit
        #Expand upper and lower limits by limit_normals from reference range if marked so.
        if list_item.use_lln or list_item.use_uln:
            list_item = self.expand_list_limit(list_item)
        if list_item:
            val, lower_limit, upper_limit = self.round_off(value, list_item)
            if eval(eval_str.format(val=val,
                                    value_low_quantifier=list_item.value_low_quantifier,
                                    lower_limit=lower_limit,
                                    value_high_quantifier=list_item.value_high_quantifier,
                                    upper_limit=upper_limit)):
                flag = list_item.grade
        return flag, lower_limit, upper_limit

    def expand_list_limit(self, list_item):
        #pdb.set_trace()
        reference_list = ('reference_range_list', get_model('lab_clinic_reference', 'ReferenceRangeListItem'))
        reference_flag = ReferenceFlag(
            self.subject_identifier,
            reference_list,
            self.test_code,
            self.gender,
            self.dob,
            self.reference_datetime,
            hiv_status=self.hiv_status,
            is_default_hiv_status=self.is_default_hiv_status)
        reference_item = reference_flag._get_list()
        if reference_item:
            if list_item.use_lln:
                list_item.value_low = list_item.value_low * reference_item[0].value_low
                list_item.value_high = list_item.value_high * reference_item[0].value_low
            elif list_item.use_uln:
                list_item.value_low = list_item.value_low * reference_item[0].value_high
                list_item.value_high = list_item.value_high * reference_item[0].value_high
            else:
                list_item = None
        else:
            list_item = None
        return list_item