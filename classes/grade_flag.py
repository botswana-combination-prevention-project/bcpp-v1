from django.db.models import Q
from django.conf import settings
from bhp_lab_tracker.classes import lab_tracker
from lab_flag.classes import Flag


class GradeFlag(Flag):

    def __init__(self, reference_list, test_code, subject_identifier, gender, dob, reference_datetime, **kwargs):
        hiv_status = kwargs.get('hiv_status', None)
        is_default_hiv_status = kwargs.get('is_default_hiv_status', None)
        if not hiv_status:
            subject_identifier, hiv_status, reference_datetime, is_default_hiv_status = lab_tracker.get_value(self.get_lab_tracker_group_name(), subject_identifier, reference_datetime)
        if not hiv_status:
            raise TypeError('hiv_status cannot be None.')
        super(GradeFlag, self).__init__(reference_list, test_code, gender, dob, reference_datetime, hiv_status, is_default_hiv_status, **kwargs)

    def get_lab_tracker_group_name(self):
        """Returns a group name to use when filtering on values in the lab_tracker class.

        See :mode:bhp_lab_tracker"""
        return 'HIV'

    def get_list_prep(self, test_code, gender, hiv_status):
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
        return list_items

    def get_evaluate_prep(self, value, list_item):
        """ Determines if the value falls within one of the graded ranges."""
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

