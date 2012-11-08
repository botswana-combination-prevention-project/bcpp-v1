import logging
import re
from datetime import datetime
from bhp_common.utils import get_age_in_days
from lab_test_code.models import BaseTestCode
from lab_reference.models import BaseReferenceListItem
from bhp_lab_tracker.classes import lab_tracker

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Flag(object):

    def __init__(self, subject_identifier, reference_list, test_code, gender, dob, drawn_datetime, release_datetime, **kwargs):
        self.dirty = False
        self.group_name = 'HIV'  # lab_tracker cls group name
        self.list_name, self.list_item_model_cls = reference_list
        self.test_code = test_code
        if not isinstance(test_code, BaseTestCode):
            raise TypeError('Parameter \'test_code\' must be an instance of \'BaseTestCode\'.')
        self.subject_identifier = subject_identifier
        self.gender = gender
        self.dob = dob
        self.drawn_datetime = drawn_datetime
        self.release_datetime = release_datetime
        # age is relative to the date sample drawn!!
        self.age_in_days = get_age_in_days(self.drawn_datetime, self.dob)
        self.hiv_status = kwargs.get('hiv_status', None)
        self.is_default_hiv_status = kwargs.get('is_default_hiv_status', None)
        if not self.hiv_status:
            self.get_hiv_status()
        if not self.hiv_status:
            raise TypeError('hiv_status cannot be None.')

    def get_hiv_status(self):
        """ Returns the HIV status known at the time of sample draw."""
        if not self.hiv_status:
            # convert reference datetime to midnight
            release_datetime = datetime(self.release_datetime.year, self.release_datetime.month, self.release_datetime.day, 23, 59, 59, 999)
            self.hiv_status, self.is_default_hiv_status = lab_tracker.get_value(
                self.group_name,
                self.subject_identifier,
                release_datetime)
        if not self.hiv_status:
            raise TypeError('hiv_status cannot be None for subject {0} relative to {1} using group '
                            'name {2}.'.format(self.subject_identifier,
                                               release_datetime,
                                               self.group_name))

    def get_list_prep(self, value, test_code, gender, hiv_status, age_in_days, **kwargs):
        """Returns a filtered list of list items .

        Users should override this."""
        raise TypeError('No reference list has been associated with this class. Cannot continue')

    def get_evaluate_prep(self, value, list_item):
        """Returns a tuple of the calculated flag, lower limit, upper limit.

        Users should override this."""
        return None, None, None

    def check_list_prep(self, list_items):
        """Runs additional checks for the reference table.

        Users may override."""
        return None

    def order_list_prep(self, list_items):
        """Returns an ordered list of list_items.

        Users may override."""
        return list_items

    def get_list(self, value=None):
        """Returns the items from the reference list that meet the criteria of test code, gender, hiv status and age.

        Calls the user defined :func:`get_list_prep` to get the list then checks that there are no duplicates
        in the upper or lower ranges."""
        list_items = [list_item for list_item in self.get_list_prep(value, self.test_code, self.gender, self.hiv_status, self.age_in_days)]
        for index, list_item in enumerate(list_items):
            if not list_item.active:
                raise TypeError('Inactive List item returned from get_list_prep(). Got {0}'.format(list_item))
            list_items[index] = self.modify_list_item(list_item)
        if list_items:
            self.check_list_prep(list_items)
            # list may need to be ordered as in the case of grading.
            list_items = self.order_list_prep(list_items)
        return list_items

    def modify_list_item(self, list_item):
        """Modifies a list_item in some way."""
        return list_item

    def evaluate(self, value):
        """ Determines the flag for value and returns a with the flag and related parameters.

        .. note:: If an value is evaluated but not of a gradable range, flag = 0. If 
                  the value / test code cannot be evaluated for lack of grade items, the
                  flag is None.

        .. note:: If list is ordered then the list item selected is predictable.
        .. seealso:: :func:`order_list_prep`"""
        if self.dirty:
            raise ValueError('Instance has already been evaluated. Initialize a new instance before evaluating again.')
        if not isinstance(value, (int, float, long)):
            raise TypeError('Value must be an instance of int, float, long.')
        retdict = {}
        # retdict.update({'is_default_hiv_status': self.is_default_hiv_status})
        # get the reference list from the user defined method
        list_items = self.get_list(value)
        #if not list_items:
        #    # nothing in the reference list for this
        #    logger.warning('    No matching {0} items for {1}={2} ({3}).'.format(self.list_name, self.test_code.code, value, self.get_joined_criteria()))
        if list_items:
            for list_item in list_items:
                flag = 0  # default to 0. This item is evaluated but not gradeable. 
                if not isinstance(list_item, BaseReferenceListItem):
                    raise TypeError('List item must be an instance of BaseReferenceListItem.')
                if not list_item.dummy:  # ignore a record marked as dummy
                    # call user defined evaluate
                    flag, lower_limit, upper_limit = self.get_evaluate_prep(value, list_item)
                    if flag:
                        retdict = {'flag': flag, 'lower_limit': lower_limit, 'upper_limit': upper_limit}
                        # takes the first list_item that matches.
                        # if list_items is ordered then this is predicatable
                        break
        self._cleanup()
        return retdict

    def get_joined_criteria(self):
        return ' '.join([self.subject_identifier, self.gender, self.hiv_status, 'days=' + str(self.age_in_days)])

    def filter_list_items_by_age(self, list_items, age_in_days):
        """ Filters list items for this subject's age and populates a list of list_item instances."""
        my_list_items = []
        eval_str = '{age_in_days} {age_low_quantifier} {age_low_days} and {age_in_days} {age_high_quantifier} {age_high_days}'
        for list_item in list_items:
            if not re.match('^\>$|^\>\=$', list_item.age_low_quantifier.strip(' \t\n\r')):
                raise TypeError('Invalid age_low_quantifier in reference list for {0}. Got {1}.'.format(list_item.test_code.code, list_item.age_low_quantifier))
            if not re.match('^\<$|^\<\=$', list_item.age_high_quantifier.strip(' \t\n\r')):
                raise TypeError('Invalid age_high_quantifier in reference list for {0}. Got {1}.'.format(list_item.test_code.code, list_item.age_high_quantifier))
            if eval(eval_str.format(age_in_days=age_in_days,
                                    age_low_quantifier=list_item.age_low_quantifier,
                                    age_low_days=list_item.age_low_days(),
                                    age_high_quantifier=list_item.age_high_quantifier,
                                    age_high_days=list_item.age_high_days())):
                my_list_items.append(list_item)
        # return a list, not a queryset
        return my_list_items

    def round_off(self, value, list_item):
        """Rounds off value and reference range to the number of places from "test code" for valid comparison."""
        #flag, lower_limit, upper_limit = None, None, None
        places = self.test_code.display_decimal_places or 0  # this might be worth a warning in None
        lower_limit = round(list_item.value_low, places)
        upper_limit = round(list_item.value_high, places)
        value = round(value, places)
        return value, lower_limit, upper_limit

    def _cleanup(self):
        """ Clean up instance variables in case you forget to re-init."""
        self.dirty = True
        self.test_code = None
        self.gender = None
        self.dob = None
        self.release_datetime = None
        self.drawn_datetime = None
        self.hiv_status = None
        self.is_default_hiv_status = None
        self.age_in_days = None
