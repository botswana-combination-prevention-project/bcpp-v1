from lab_reference.classes import ReferenceFlag


class ClinicReferenceFlag(ReferenceFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.registered_subject.gender
        dob = result_item.result.order.aliquot.receive.registered_subject.dob
        reference_datetime = result_item.result.order.aliquot.receive.receive_datetime
        subject_identifier = result_item.result.order.aliquot.receive.registered_subject.subject_identifier
        hiv_status, is_default_hiv_status = self.get_hiv_status(
            subject_identifier,
            reference_datetime, **kwargs)
        super(ClinicReferenceFlag, self).__init__(
            reference_list,
            test_code,
            subject_identifier,
            gender,
            dob,
            reference_datetime,
            hiv_status=hiv_status,
            is_default_hiv_status=is_default_hiv_status)
