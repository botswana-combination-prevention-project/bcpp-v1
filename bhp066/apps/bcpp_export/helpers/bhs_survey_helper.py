from . import BHSBaseExport


class BHSSurveyHelper(BHSBaseExport):

    def __init__(self):

        self._has_tested = None
        self._has_record = None
        self._when_hiv_test = None
        self._verbal_hiv_result = None
        self._hiv_test_date = None
        self._other_record = None
        self._pima_today = None
        self._pima_today_other = None
        self._cd4_value = None
        self._on_arv = None
        self._ever_taken_arv = None
        self._arv_naive = None
        self._arv_evidence = None
        self._circumcised = None
        self._uncircumcised = None
        self._referral_clinic = None
        self._referral_clinic_other = None
        self._referral_code = None
        self._referral_date = None
        self._referral_appt_date = None
        self._subject_locator = None
        self._home_visit_permission = None
        self._hiv_testing_history = None
        self._anc_reg = None
        self._last_hiv_care_pos = None
        self._pima = None
        self._currently_pregnant = None
        self._recorded_hiv_result = None
        self._hiv_result = None
        self._preg_arv = None
        self._hiv_care_adherence = None
        self._viral_load = None

    @property
    def referral_code(self):
        """ returns referral code, referred for  """
        return self._referral_code

    @property
    def referral_date(self):
        """ returns date of referral from subject_subjectreferral """
        return self._referral_date

    @property
    def referral_appt_date(self):
        """ returns referral appointment date from subject_subjectreferral """
        return self._referral_appt_date

    @property
    def referral_clinic(self):
        """ returns referral clinic """
        return self._referral_clinic

    @property
    def referral_clinic_other(self):
        """ returns referral clinic other """
        return self._referral_clinic_other

    @property
    def subject_locator(self):
        """ returns subject locator """
        return self._subject_locator

    @property
    def home_visit_permission(self):
        return self._home_visit_permission

    @property
    def contact_someone(self):
        return self._contact_someone

    @property
    def recorded_hiv_result(self):
        """ returns document hiv test result """
        return self._recorded_hiv_result

    @property
    def other_hiv_documentation_date(self):
        pass

    @property
    def why_no_hivtest(self):
        """ returns why not tested , source model: bcpp_subject_hivtested """
        pass

    @property
    def last_hiv_care_pos(self):
        """ returns where last went for care(HIV+) """
        return self._last_hiv_care_pos

    @property
    def pima(self):
        """ returns pima """
        return self._pima

    @property
    def circumcision(self):
        """ returns circumcision , source model: bcpp_subject_circumision """
        pass

    @property
    def currently_pregnant(self):
        """ returns pregnant status, source model: bcpp_subject_reproductivehealth """
        return self._currently_pregnant

    @property
    def hiv_result(self):
        """ returns Today's HIV result """
        return self._hiv_result

    @property
    def preg_arv(self):
        """ returns ANC info: preg_arv """
        return self._preg_arv

    @property
    def anc_reg(self):
        """ returns ANC info: anc_reg """
        return self._anc_reg

    @property
    def hiv_care_adherence(self):
        """ returns hiv_care_adherence source model: hiv_care_adherence """
        return self._hiv_care_adherence

    @property
    def on_arv(self):
        """ returns treatment status source model: hiv_care_adherence"""
        return self._on_arv

    @property
    def ever_taken_arv(self):
        """ returns treatment status source model: hiv_care_adherence"""
        return self._ever_taken_arv

    @property
    def arv_naive(self):
        """ returns treatment status source model: hiv_care_adherence """
        return self._arv_naive

    @property
    def arv_evidence(self):
        return self._arv_evidence

    @property
    def hiv_testing_history(self):
        """ returns hiv_testing_history """
        return self._hiv_testing_history

    @property
    def has_tested(self):
        """ returns Has Tested from subject_hivtestinghistory"""
        return self._has_tested

    @property
    def has_record(self):
        """ returns has record from subject_hivtestinghistory"""
        return self._has_record

    @property
    def when_hiv_test(self):
        """ returns self-reported hiv test date from subject_hivtestinghistory"""
        return self._when_hiv_test

    @property
    def verbal_hiv_result(self):
        """ returns self-reported hiv test result from subject_hivtestinghistory"""
        return self._verbal_hiv_result

    @property
    def hiv_test_date(self):
        """ returns document hiv test date from subject_hivtestinghistory"""
        return self._hiv_test_date

    @property
    def pima_today(self):
        """ returns CD4 Test Today from subject_pima"""
        return self._pima_today

    @property
    def pima_today_other(self):
        """ returns CD4 Test Today from  subject_pima """
        return self._pima_today_other

    @property
    def cd4_value(self):
        """ returns CD4 Value from subject_pima """
        return self._cd4_value

    @property
    def circumcised(self):
        """ returns circumcised from subject_circumcision """
        return self._circumcised

    @property
    def uncircumcised(self):
        """ returns MC Status from subject_uncircumcised """
        return self._uncircumcised

    @property
    def viral_load(self):
        """ return viral load """
        return self._viral_load
