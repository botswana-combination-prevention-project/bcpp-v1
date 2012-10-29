import logging
from bhp_common.utils import get_age_in_days
from lab_test_code.models import BaseTestCode
from lab_reference.models import BaseReferenceListItem

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Flag(object):

    def __init__(self, reference_list, test_code, gender, dob, reference_datetime, hiv_status, is_default_hiv_status):
        self.dirty = False
        self.list_name, self.list_item_model_cls = reference_list
        self.test_code = test_code
        if not isinstance(test_code, BaseTestCode):
            raise TypeError('Parameter \'test_code\' must be an instance of \'BaseTestCode\'.')
        self.gender = gender
        self.dob = dob
        self.reference_datetime = reference_datetime
        self.hiv_status = hiv_status
        self.is_default_hiv_status = is_default_hiv_status
        self.age_in_days = get_age_in_days(self.reference_datetime, self.dob)

    def get_list_prep(self, *args):
        """Returns a filtered list of list items .

        Users should override this."""
        raise TypeError('No reference list has been associated with this class. Cannot continue')

    def get_evaluate_prep(self, value, list_item):
        """Returns a tuple of the calculated flag, lower limit, upper limit.

        Users should override this."""
        return None, None, None

    def evaluate(self, value):
        """ Determines the flag for value and returns a with the flag and related parameters."""
        if self.dirty:
            raise ValueError('Instance has already been evaluated. Initialize a new instance before evaluating again.')
        if not isinstance(value, (int, float, long)):
            raise TypeError('Value must be an instance of int, float, long.')
        retdict = {}
        retdict.update({'is_default_hiv_status': self.is_default_hiv_status})
        # get the reference list from the user defined method
        list_items = self.get_list_prep(test_code, gender, hiv_status)
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
