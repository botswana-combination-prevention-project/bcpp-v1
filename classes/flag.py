import logging
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

    def __init__(self, subject_identifier, reference_list, test_code, gender, dob, reference_datetime, **kwargs):
        self.dirty = False
        self.group_name = 'HIV'  # lab_tracker cls group name
        self.list_name, self.list_item_model_cls = reference_list
        self.test_code = test_code
        if not isinstance(test_code, BaseTestCode):
            raise TypeError('Parameter \'test_code\' must be an instance of \'BaseTestCode\'.')
        self.subject_identifier = subject_identifier
        self.gender = gender
        self.dob = dob
        self.reference_datetime = reference_datetime
        self.age_in_days = get_age_in_days(self.reference_datetime, self.dob)
        self.hiv_status = kwargs.get('hiv_status', None)
        self.is_default_hiv_status = kwargs.get('is_default_hiv_status', None)
        if not self.hiv_status:
            self.get_hiv_status()
        if not self.hiv_status:
            raise TypeError('hiv_status cannot be None.')

    def get_hiv_status(self):
        """ """
        if not self.hiv_status:
            self.hiv_status, self.is_default_hiv_status = lab_tracker.get_value(
                self.group_name,
                self.subject_identifier,
                self.reference_datetime)
        if not self.hiv_status:
            raise TypeError('hiv_status cannot be None for subject {0} relative to {1} using group name {2}.'.format(self.subject_identifier,
                                                                                                                     self.reference_datetime,
                                                                                                                     self.group_name))

    def get_list_prep(self, test_code, gender, hiv_status, age_in_days):
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

    def _get_list(self):
        """Returns the items from the reference list that meet the criteria of test code, gender, hiv status and age.

        Calls the user defined :func:`get_list_prep` to get the list then checks that there are no duplicates
        in the upper or lower ranges."""
        list_items = self.get_list_prep(self.test_code, self.gender, self.hiv_status, self.age_in_days)
        if not list_items:
            raise TypeError('No reference list found for test code {0} gender {1} hiv status {2}. Cannot continue'.format(self.test_code, self.gender, self.hiv_status))
        # inspect items for possible duplicates, overlapping ranges and for missing grades
        upper_ranges = []
        lower_ranges = []
        for list_item in list_items:
            upper_ranges.append(list_item.uln)
            lower_ranges.append(list_item.lln)
        if upper_ranges != list(set(upper_ranges)) or lower_ranges != list(set(lower_ranges)):
            raise TypeError('Duplicates lower or upper bounds detected in reference list for test code {0} gender {1} hiv status {2}. Age is {3}.'.format(self.test_code, self.gender, self.hiv_status, self.age_in_days))
        self.check_list_prep(list_items)
        # list may need to be ordered as in the case of grading.
        list_items = self.order_list_prep(list_items)
        return list_items

    def evaluate(self, value):
        """ Determines the flag for value and returns a with the flag and related parameters.

        .. note:: If list is ordered then the list item selected is predictable.
        .. seealso:: :func:`order_list_prep`"""
        if self.dirty:
            raise ValueError('Instance has already been evaluated. Initialize a new instance before evaluating again.')
        if not isinstance(value, (int, float, long)):
            raise TypeError('Value must be an instance of int, float, long.')
        retdict = {}
        # retdict.update({'is_default_hiv_status': self.is_default_hiv_status})
        # get the reference list from the user defined method
        list_items = self._get_list()
        if not list_items:
            # nothing in the reference list for this
            logger.warning('    No {0} items for {1}.'.format(self.list_name, self.test_code.code))
        else:
            for list_item in list_items:
                if not isinstance(list_item, BaseReferenceListItem):
                    raise TypeError('List item must be an instance of BaseReferenceListItem.')
                # call user defined evaluate
                retdict['flag'], retdict['lower_limit'], retdict['upper_limit'] = self.get_evaluate_prep(value, list_item)
                if retdict['flag']:
                    # takes the first list_item that matches.
                    # if list_items is ordered then this is predicatable
                    break
        self._cleanup()
        return retdict

    def round_off(self, value, list_item):
        """Rounds off value and reference range to the number of places from "test code" for valid comparison."""
        #flag, lower_limit, upper_limit = None, None, None
        places = self.test_code.display_decimal_places or 0  # this might be worth a warning in None
        # lower_limit = ceil(list_item.lln * (10 ** places)) / (10 ** places)
        # upper_limit = ceil(list_item.uln * (10 ** places)) / (10 ** places)
        # value = ceil(value * (10 ** places)) / (10 ** places)
        lower_limit = round(list_item.lln, places)
        upper_limit = round(list_item.uln, places)
        value = round(value, places)
        return value, lower_limit, upper_limit

    def _cleanup(self):
        """ Clean up instance variables in case you forget to re-init."""
        self.dirty = True
        self.test_code = None
        self.gender = None
        self.dob = None
        self.reference_datetime = None
        self.hiv_status = None
        self.is_default_hiv_status = None
        self.age_in_days = None
