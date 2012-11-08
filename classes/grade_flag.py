from lab_grading.classes import GradeFlag as BaseGradeFlag


class GradeFlag(BaseGradeFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.patient.gender
        dob = result_item.result.order.aliquot.receive.patient.dob
        hiv_status = result_item.result.order.aliquot.receive.patient.hiv_status
        drawn_datetime = result_item.result.order.aliquot.receive.receive_datetime
        release_datetime = result_item.result_item_datetime
        subject_identifier = result_item.result.subject_identifier
        super(GradeFlag, self).__init__(subject_identifier, reference_list, test_code, gender, dob, drawn_datetime, release_datetime, hiv_status, **kwargs)
