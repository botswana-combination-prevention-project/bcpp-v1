import re
from django.conf import settings
from lab_flag.classes import Flag
import pdb

class ReferenceFlag(Flag):

    def check_list_prep(self, list_items):
        """Runs additional checks for the reference table."""
        """For reference_flag only a single comparison item should be exist."""
        ranges = []
        for list_item in list_items:
            ranges.append(str(list_item.lln)+'-'+str(list_item.uln))
            ranges = list(ranges)
        if len(ranges) != 1:
            raise TypeError('Multiple reference ranges for test code {0} gender {2}. Got ranges for "{3}".'.format(self.test_code, self.gender, ranges))

    def get_list_prep(self, test_code, gender, hiv_status, age_in_days):
        """Returns a filtered list of list items."""
        list_items = self.list_item_model_cls.objects.filter(
            **{'{0}__name__iexact'.format(self.list_name): settings.REFERENCE_RANGE_LIST,
               'test_code': test_code,
               'gender__iexact': gender})
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
        return my_list_items

    def get_evaluate_prep(self, value, list_item):
        """ Determines if the value falls outside of the reference range after all values are rounded up."""
        flag = None
        val, lln, uln = self.round_off(value, list_item)
        return self.get_flg(val, lln, uln, flag)

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
