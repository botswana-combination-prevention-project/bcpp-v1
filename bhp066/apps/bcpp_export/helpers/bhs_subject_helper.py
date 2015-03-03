from .bhs_base_export import BHSBaseExport


class BHSSubjectHelper(BHSBaseExport):

    def __init__(self):
        self._omang_number = None
        self._first_name = None
        self._last_name = None
        self._date_of_birth = None
        self._gender = None

    @property
    def omang_number(self):
        """Returns Omang number."""
        return self._omang_number

    @property
    def first_name(self):
        """Returns First name."""
        return self._first_name

    @property
    def last_name(self):
        """Returns Last name."""
        return self._last_name

    @property
    def date_of_birth(self):
        """Returns date of birth."""
        return self._date_of_birth

    @property
    def gender(self):
        """Returns gender."""
        return self._gender
