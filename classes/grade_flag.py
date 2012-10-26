from math import ceil
from django.db.models import Q
from django.conf import settings
from lab_flag.classes import Flag
import pdb


class GradeFlag(Flag):

    def get_list_prep(self):
        """Returns a filtered list of GradingListItem for this ."""
        if self.hiv_status:
            qset = (Q(hiv_status__iexact=self.hiv_status.lower()) | Q(hiv_status__iexact='ANY'))
        else:
            qset = (Q(hiv_status__iexact='ANY'))
        list_items = self.list_item_model_cls.objects.filter(
            qset,
            **{'{0}__name__iexact'.format(self.list_name): settings.GRADING_LIST,
               'grading_list__name__iexact': settings.GRADING_LIST,
               'test_code': self.test_code,
               'gender__icontains': self.gender})
        return list_items

    def get_evaluate_prep(self, value, list_item):
        """ Determines if the value falls within one of the graded ranges."""
        # pdb.set_trace()
        flag, lower_limit, upper_limit = None, None, None
        if str(list_item.age_low_quantifier) == str('> ') and str(list_item.age_high_quantifier) == str('< '):
            if self.age_in_days > list_item.age_low_days() and self.age_in_days < list_item.age_high_days():
                val, lower_limit, upper_limit = self.round_off(value, list_item)
                if val >= lower_limit and val <= upper_limit:
                    flag = list_item.grade
                return flag, lower_limit, upper_limit
        elif str(list_item.age_low_quantifier) == str('> ') and str(list_item.age_high_quantifier) == str('<='):
            if self.age_in_days > list_item.age_low_days() and self.age_in_days <= list_item.age_high_days():
                val, lower_limit, upper_limit = self.round_off(value, list_item)
                if val >= lower_limit and val <= upper_limit:
                    flag = list_item.grade
                return flag, lower_limit, upper_limit
        elif str(list_item.age_low_quantifier) == str('>=') and str(list_item.age_high_quantifier) == str('< '):
            if self.age_in_days >= list_item.age_low_days() and self.age_in_days < list_item.age_high_days():
                val, lower_limit, upper_limit = self.round_off(value, list_item)
                if val >= lower_limit and val <= upper_limit:
                    flag = list_item.grade
                return flag, lower_limit, upper_limit
        elif str(list_item.age_low_quantifier) == str('>=') and str(list_item.age_high_quantifier) == str('<='):
            if self.age_in_days >= list_item.age_low_days() and self.age_in_days <= list_item.age_high_days():
                val, lower_limit, upper_limit = self.round_off(value, list_item)
                if val >= lower_limit and val <= upper_limit:
                    flag = list_item.grade
                return flag, lower_limit, upper_limit
        return flag, lower_limit, upper_limit


#        if list_item.age_low_days() <= self.age_in_days and list_item.age_high_days() >= self.age_in_days:
#            # round up all values
#            places = self.test_code.display_decimal_places or 0  # this might be worth a warning in None
#            lower_limit = ceil(list_item.lln * (10 ** places)) / (10 ** places)
#            upper_limit = ceil(list_item.uln * (10 ** places)) / (10 ** places)
#            value = ceil(value * (10 ** places)) / (10 ** places)
#            if value >= lower_limit and value <= upper_limit:
#                flag = list_item.grade
#        return flag, lower_limit, upper_limit

