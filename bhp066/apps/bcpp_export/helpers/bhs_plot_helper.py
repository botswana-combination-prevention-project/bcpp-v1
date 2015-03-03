from . import BHSBaseExport


class BhsPlotHelper(BHSBaseExport):

    def __init__(self):
        self._offered = None
        self._refusal_reason = None
        self._report_datetime = None
        self._received_htc_date = None
        self._confirmed = None
        self._visit_time = None
        self._time_of_day = None
        self._gps_latitude = None
        self._gps_longitude = None
        self._household_count = None

    @property
    def plot_status(self):
        """ returns plot status"""
        return self._plot_status

    @property
    def confirmed(self):
        """ returns confirmed """
        return self._confirmed

    @property
    def visit_time(self):
        """ Time of Visit (The Visit That Determined Plot Status) """
        return self._visit_time

    @property
    def time_of_day(self):
        """ Time of day"""
        return self._time_of_day

    @property
    def gps_latitude(self):
        """ GPS latitude """
        return self._gps_latitude

    @property
    def gps_longitude(self):
        """ GPS longitude """
        return self._gps_longitude

    @property
    def household_count(self):
        """ Household Count """
        return self._household_count

#     @property
#     def handed_to_htc(self):
#         """ """
#         return self._handed_to_htc
