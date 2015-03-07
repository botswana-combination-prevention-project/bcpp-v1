from .plot import Plot


class Enumeration(object):

    def __init__(self):

        self.identity = None
        self.citizen = None
        self.legal_marriage = None
        self._age_in_years = None
        self._gender = None
        self._member_status = None
        self._created = None
        self._status_fuv1 = None
        self._status_fuv2 = None
        self._status_fuv3 = None
        self._absent = None
        self._enumeration_created = None
        self._relation = None
        self._nights_away = None
        self._permanent_resident = None
        self._part_time_resident

    @property
    def age_in_years(self):
        """Returns age in years from enumeration data or, if exists, from the consent. """
        return self._age_in_years

    @property
    def gender(self):
        """ returns gender from household_household_member"""
        return self._gender

    @property
    def member_status(self):
        """ returns member status from household_member_member"""
        return self._member_status

    @property
    def status_fuv1(self):
        """ returns Status in FUV1 """
        return self._status_fuv1

    @property
    def status_fuv2(self):
        """ returns Status in FUV2 """
        return self._status_fuv2

    @property
    def status_fuv3(self):
        """ returns Status in FUV3 """
        return self._status_fuv3

    @property
    def created(self):
        """ returns family members joining during follow up, model: household_householdmember_audit"""
        return self._created

    @property
    def absent(self):
        """ returns present status during enumeration """
        return self._absent

    @property
    def enumeration_created(self):
        """ returns enumeration created date """
        return self._enumeration_created

    @property
    def relation(self):
        """ returns relationship to head of household during bhs """
        return self._relation

    @property
    def nights_away(self):
        """ returns nights away, source model: subject_residencymobility """
        return self._nights_away

    @property
    def permanent_resident(self):
        """ returns permanent_resident, source model: subject_residencymobility """
        return self._permanent_resident

    @property
    def part_time_resident(self):
        """ part-time resident, source model: subject_enrollment """
        return self._part_time_resident
