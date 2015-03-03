from . import BHSBaseExport


class BhsHTCHelper(BHSBaseExport):

    def __init__(self):
        self._offered = None
        self._refusal_reason = None
        self._report_datetime = None
        self._received_htc_date = None

    @property
    def offered(self):
        """ returns offered HTC only service """
        return self._offered

    @property
    def refusal_reason(self):
        """ returns reasons for refusal , source model: household_member_subjecthtc"""
        return self._refusal_reason

    @property
    def report_datetime(self):
        """ returns date of offering HTC only service , source model: household_member_subjecthtc"""
        return self._report_datetime

    @property
    def received_htc_date(self):
        """ returns date of receiving htc """
        return self._received_htc_date
