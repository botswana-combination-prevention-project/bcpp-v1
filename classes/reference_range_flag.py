from lab_reference.classes import ReferenceFlag


class ReferenceRangeFlag(ReferenceFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.patient.gender
        dob = result_item.result.order.aliquot.receive.patient.dob
        reference_datetime = result_item.result.order.aliquot.receive.receive_datetime
        hiv_status = result_item.result.order.aliquot.receive.patient.hiv_status
        super(ReferenceRangeFlag, self).__init__(reference_list, test_code, gender, dob, reference_datetime, hiv_status, **kwargs)
