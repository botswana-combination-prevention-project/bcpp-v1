from . import BHSBaseExport

class BHSSubjectHelper(BHSBaseExport):

    def __init__(self):
        self._omang_number = None
        self._first_name = None
        self._last_name = None
        self._date_of_birth = None
        self._gender = None

    @property
    def omang_number(self):
        """returns Omang number"""
        return self._omang_number

    @property
    def first_name(self):
        """returns First name"""
        return self._first_name

    @property
    def last_name(self):
        """returns Last name"""
        return self._last_name

    @property
    def date_of_birth(self):
        """Returns date of birth"""
        return self._date_of_birth

    @property
    def gender(self):
        """Returns gender"""
        return self._gender