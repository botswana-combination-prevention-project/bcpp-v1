import re
from django.db.models import Q
from django.conf import settings
from lab_flag.classes import Flag


class GradeFlag(Flag):

    def check_list_prep(self, list_items):
        """Runs additional checks for the reference table."""
        grades = []
        for list_item in list_items:
            grades.append(list_item.grade)
        grades = list(set(grades))
        grades.sort()
        if grades != [1, 2, 3, 4]:
            raise TypeError('Missing ranges for grade in reference list for test code {0} gender {1} hiv status {2}. Got ranges for "{3}".'.format(self.test_code, self.gender, self.hiv_status, grades))

    def get_lab_tracker_group_name(self):
        """Returns a group name to use when filtering on values in the lab_tracker class.

        See :mode:bhp_lab_tracker"""
        return 'HIV'

    def get_list_prep(self, test_code, gender, hiv_status, age_in_days):
        """Returns a filtered list of GradingListItem for this ."""
        if hiv_status:
            qset = (Q(hiv_status__iexact=hiv_status.lower()) | Q(hiv_status__iexact='ANY'))
        else:
            qset = (Q(hiv_status__iexact='ANY'))
        list_items = self.list_item_model_cls.objects.filter(
            qset,
            **{'{0}__name__iexact'.format(self.list_name): settings.GRADING_LIST,
               'grading_list__name__iexact': settings.GRADING_LIST,
               'test_code': test_code,
               'gender__icontains': gender})
        # filter list items for this subject's age
        my_list_items = []
        eval_str = '{age_in_days} {age_low_quantifier} {age_low_days} and {age_in_days} {age_high_quantifier} {age_high_days}'
        for list_item in list_items:
            if not re.match('^\>$|^\>\=$', list_item.age_low_quantifier.strip(' \t\n\r')):
                raise TypeError('Invalid age_low_quantifier in reference list. Got {0}.'.format(list_item.age_low_quantifier))
            if not re.match('^\<$|^\<\=$', list_item.age_high_quantifier.strip(' \t\n\r')):
                raise TypeError('Invalid age_high_quantifier in reference list. Got {0}.'.format(list_item.age_high_quantifier))
            if eval(eval_str.format(age_in_days=self.age_in_days,
                                    age_low_quantifier=list_item.age_low_quantifier,
                                    age_low_days=list_item.age_low_days(),
                                    age_high_quantifier=list_item.age_high_quantifier,
                                    age_high_days=list_item.age_high_days())):
                my_list_items.append(list_item)
            if list_item in my_list_items:
                print ' * {0}'.format(list_item.describe())
            else:
                print '   {0}'.format(list_item.describe())
        return my_list_items

    def get_evaluate_prep(self, value, list_item):
        """ Determines if the value falls within one of the graded ranges."""
        eval_str = '{val} {lln_quantifier} {lower_limit} and {val} {uln_quantifier} {upper_limit}'
        flag = None
        val, lower_limit, upper_limit = self.round_off(value, list_item)
        if eval(eval_str.format(val=val,
                                lln_quantifier=list_item.lln_quantifier,
                                lower_limit=lower_limit,
                                uln_quantifier=list_item.uln_quantifier,
                                upper_limit=upper_limit)):
            flag = list_item.grade
        return flag, lower_limit, upper_limit
