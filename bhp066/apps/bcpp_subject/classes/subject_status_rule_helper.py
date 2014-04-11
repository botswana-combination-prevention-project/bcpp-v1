from .subject_status_helper import SubjectStatusHelper


class SubjectStatusRuleHelper(SubjectStatusHelper):

    @property
    def hiv_result_required(self):
        if self.todays_hiv_result:
            return True
        if not self.hiv_result:
            return True
        if self.hiv_result:
            return self.hiv_result in ['POS', 'NEG']

    @property
    def pima_required(self):
        return self.on_art == False
