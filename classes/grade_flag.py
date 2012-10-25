from lab_grading.classes import GradeFlag as BaseGradeFlag
from bhp_lab_tracker.classes import lab_tracker


class GradeFlag(BaseGradeFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.registered_subject.gender
        dob = result_item.result.order.aliquot.receive.registered_subject.dob
        reference_datetime = result_item.result.order.aliquot.receive.receive_datetime
        hiv_status = result_item.result.order.aliquot.receive.registered_subject.hiv_status
        super(GradeFlag, self).__init__(reference_list, test_code, gender, dob, reference_datetime, hiv_status, **kwargs)
