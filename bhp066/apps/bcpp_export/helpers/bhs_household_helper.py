from . import BHSBaseExport


class BhsHouseholdHelper(BHSBaseExport):

    def __init__(self):

        self._enumerated = None
        self._action = None
        self._legal_marriage = None
        self._created = None
        self._replaced_by = None
        self._tfv_fuv1 = None
        self._tfv_fuv2 = None
        self._rfr_ess = None
        self._enrolled = None

    @property
    def household_structure(self):
        """ returns household_structure """
        pass

    @property
    def enumerated(self):
        """ returns enumerated household_householdstructure """
        return self._enumerated

    @property
    def action(self):
        """ returns HH status from household_householdstructure"""
        return self._action

    @property
    def created(self):
        """ returns time of first visit(TFV) """
        return self._created

    @property
    def tfv_in_fuv1(self):
        """ """
        return self._tfv_in_fuv1

    @property
    def replaced_by(self):
        """ returns replace_by from household_household"""
        return self._replaced_by

    @property
    def reason(self):
        """ returns reason for refusal (RFR)"""
        return None

    @property
    def tfv_fuv1(self):
        """ returns tlv in FUV1"""
        return self._tfv_fuv1

    @property
    def tfv_fuv2(self):
        """ returns tlv in FUV2"""
        return self._tfv_fuv2

    @property
    def rfr_ess(self):
        """ returns RFR in ESS"""
        return self._rfr_ess

    @property
    def enrolled(self):
        """ returns enrolled """
        return self._enrolled
