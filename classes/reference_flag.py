from django.conf import settings
from lab_flag.classes import Flag
from bhp_lab_tracker.classes import lab_tracker


class ReferenceFlag(Flag):

    def __init__(self, reference_list, test_code, subject_identifier, gender, dob, reference_datetime, **kwargs):
        hiv_status = kwargs.get('hiv_status', None)
        is_default_hiv_status = kwargs.get('is_default_hiv_status', None)
        if not hiv_status:
            subject_identifier, hiv_status, reference_datetime, is_default_hiv_status = lab_tracker.get_value(self.get_lab_tracker_group_name(), subject_identifier, reference_datetime)
        if not hiv_status:
            raise TypeError('hiv_status cannot be None.')
        super(ReferenceFlag, self).__init__(reference_list, test_code, gender, dob, reference_datetime, hiv_status, is_default_hiv_status, **kwargs)

    def get_list_prep(self):
        """Returns a filtered list of list items."""
        list_items = self.list_item_model_cls.objects.filter(
            **{'{0}__name__iexact'.format(self.list_name): settings.REFERENCE_RANGE_LIST,
               'test_code': self.test_code,
               'gender__icontains': self.gender})
        return list_items

    def get_evaluate_prep(self, value, list_item):
        """ Determines if the value falls outside of the reference range after all values are rounded up."""
        flag, lln, uln = None, None, None
        if str(list_item.age_low_quantifier) == str('> ') and str(list_item.age_high_quantifier) == str('< '):
            if self.age_in_days > list_item.age_low_days() and self.age_in_days < list_item.age_high_days():
                val, lln, uln = self.round_off(value, list_item)
                return self.get_flg(val, lln, uln, flag)
        elif str(list_item.age_low_quantifier) == str('> ') and str(list_item.age_high_quantifier) == str('<='):
            if self.age_in_days > list_item.age_low_days() and self.age_in_days <= list_item.age_high_days():
                val, lln, uln = self.round_off(value, list_item)
                return self.get_flg(val, lln, uln, flag)
                # flag should be None, LO or HI -- but not ''
                return flag, lln, uln
        elif str(list_item.age_low_quantifier) == str('>=') and str(list_item.age_high_quantifier) == str('< '):
            if self.age_in_days >= list_item.age_low_days() and self.age_in_days < list_item.age_high_days():
                val, lln, uln = self.round_off(value, list_item)
                return self.get_flg(val, lln, uln, flag)
                # flag should be None, LO or HI -- but not ''
                return flag, lln, uln
        elif str(list_item.age_low_quantifier) == str('>=') and str(list_item.age_high_quantifier) == str('<='):
            if self.age_in_days >= list_item.age_low_days() and self.age_in_days <= list_item.age_high_days():
                val, lln, uln = self.round_off(value, list_item)
                return self.get_flg(val, lln, uln, flag)
#        if list_item.age_low_days() <= self.age_in_days and list_item.age_high_days() >= self.age_in_days:
#            # round up all values
#            places = self.test_code.display_decimal_places or 0  # might be worth a warning if None
#            lln = ceil(list_item.lln * (10 ** places)) / (10 ** places)
#            uln = ceil(list_item.uln * (10 ** places)) / (10 ** places)
#            value = ceil(value * (10 ** places)) / (10 ** places)
#            # evaluate
#            if not flag:
#                flag = ''
#            if value < lln:
#                flag += 'LO'
#            if value > uln:
#                flag += 'HI'
#            if len(flag) > 2:
#                raise ValueError('Reference ranges overlap (HI/LO) for test code {0} age {1} gender {2}.'.format(self.test_code.code, self.age_in_days, self.gender))
#            if flag == '':
#                flag = None
        # flag should be None, LO or HI -- but not ''
        return flag, lln, uln

    def get_flg(self, val, lln, uln, flg):
        if not flg:
            flg = ''
        if val < lln:
            flg += 'LO'
        if val > uln:
            flg += 'HI'
        if len(flg) > 2:
            raise ValueError('Reference ranges overlap (HI/LO) for test code {0} age {1} gender {2}.'.format(self.test_code.code, self.age_in_days, self.gender))
        if flg == '':
            flg = None
        # flag should be None, LO or HI -- but not ''
        return flg, lln, uln

#    def round_off(self, value, list_item):
#        flag, lln, uln = None, None, None
#        places = self.test_code.display_decimal_places or 0  # might be worth a warning if None
#        lln = ceil(list_item.lln * (10 ** places)) / (10 ** places)
#        uln = ceil(list_item.uln * (10 ** places)) / (10 ** places)
#        value = ceil(value * (10 ** places)) / (10 ** places)
        # evaluate
