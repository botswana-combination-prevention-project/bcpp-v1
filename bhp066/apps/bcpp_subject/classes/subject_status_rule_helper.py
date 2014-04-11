from .subject_status_helper import SubjectStatusHelper


class SubjectStatusRuleHelper(SubjectStatusHelper):

    @property
    def hiv_result_required(self):
        if self.todays_hiv_result:
            return True
        return False if (self.new_pos == False) else True

    @property
    def pima_required(self):
        return self.on_art == False
