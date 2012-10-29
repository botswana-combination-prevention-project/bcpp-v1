from lab_reference.classes import ReferenceFlag


class ClinicReferenceFlag(ReferenceFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.registered_subject.gender
        dob = result_item.result.order.aliquot.receive.registered_subject.dob
        reference_datetime = result_item.result.order.aliquot.receive.receive_datetime
        hiv_status = result_item.result.order.aliquot.receive.registered_subject.hiv_status
        super(ClinicReferenceFlag, self).__init__(reference_list, test_code, gender, dob, reference_datetime, hiv_status, **kwargs)
