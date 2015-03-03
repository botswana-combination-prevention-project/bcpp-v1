from . import BHSBaseExport

class BHSCommunityHelper(BHSBaseExport):

    def __init__(self):
        self._community_id = None
        self._community_name = None
        self._community_code = None
        self._pair = None
        self._is_cpc = None
        self._bhs_start_date = None
        self._main_bhs_end_date = None
        self._bhs_mop_up_date = None
        self._fuv_1_start_date = None
        self._fuv_1_end_date = None
        self._fuv_2_start_date = None
        self._fuv_2_end_date = None
        self._ess_start_date = None
        self._ess_end_date = None

    @property
    def community_id(self):
        """Returns community id"""
        return self._community_id

    @property
    def community_name(self):
        """Return community name"""
        return self._community_name

    @property
    def community_code(self):
        """Return community code"""
        return self._community_code

    @property
    def pair_name(self):
        """Return village pair name"""
        return self._pair

    @property
    def cpc(self):
        """Returns True or False if community is cpc"""
        return self._is_cpc

    @property
    def bhs_start_date(self):
        """Returns main bhs start date"""
        return self._bhs_start_date

    @property
    def bhs_end_date(self):
        """Returns main bhs end date"""
        return self._main_bhs_end_date

    @property
    def bhs_mop_up_end_date(self):
        """Returns bhs mop up start date"""
        return self._bhs_mop_up_end_date

    @property
    def fuv_1_start_date(self):
        """Returns follow up visit 1 start date"""
        return self._fuv_1_end_date

    @property
    def fuv_1_end_date(self):
        """Returns follow up visit 1 end date"""
        return self._fuv_1_end_date

    @property
    def fuv_2_start_date(self):
        """Returns follow up visit 2 start date"""
        return self._fuv_2_start_date

    @property
    def fuv_2_end_date(self):
        """Returns follow up visit 2 end date"""
        return self._fuv_2_end_date

    @property
    def ess_start_date(self):
        """Returns End of Study Survey start date"""
        return self._ess_start_date

    @property
    def ess_end_date(self):
        """Returns End of Study Survey end date"""
        return self._ess_end_date