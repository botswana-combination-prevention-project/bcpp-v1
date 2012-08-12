from lab_grading.classes import GradeFlag as BaseGradeFlag


class GradeFlag(BaseGradeFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.patient.gender
        dob = result_item.result.order.aliquot.receive.patient.dob
        reference_datetime = result_item.result.order.aliquot.receive.receive_datetime
        hiv_status = result_item.result.order.aliquot.receive.patient.hiv_status
        super(GradeFlag, self).__init__(reference_list, test_code, gender, dob, reference_datetime, hiv_status, **kwargs)
