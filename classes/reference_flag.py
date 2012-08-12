from math import ceil
from django.conf import settings
from lab_flag.classes import Flag


class ReferenceFlag(Flag):

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
        if list_item.age_low_days() <= self.age_in_days and list_item.age_high_days() >= self.age_in_days:
            # round up all values
            places = self.test_code.display_decimal_places or 0  # might be worth a warning if None
            lln = ceil(list_item.lln * (10 ** places)) / (10 ** places)
            uln = ceil(list_item.uln * (10 ** places)) / (10 ** places)
            value = ceil(value * (10 ** places)) / (10 ** places)
            # evaluate
            if not flag:
                flag = ''
            if value < lln:
                flag += 'LO'
            if value > uln:
                flag += 'HI'
            if len(flag) > 2:
                raise ValueError('Reference ranges overlap (HI/LO) for test code {0} age {1} gender {2}.'.format(self.test_code.code, self.age_in_days, self.gender))
            if flag == '':
                flag = None
        #flag should be None, LO or HI -- but not ''
        return flag, lln, uln
