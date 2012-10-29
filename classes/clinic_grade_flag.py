from lab_grading.classes import GradeFlag
from bhp_lab_tracker.classes import lab_tracker


class ClinicGradeFlag(GradeFlag):

    def __init__(self, reference_list, result_item, **kwargs):
        """Extracts parameters from lab_clinic_api.ResultItem, which has a different structure to that in lab_result_item.ResultItem."""
        test_code = result_item.test_code
        gender = result_item.result.order.aliquot.receive.registered_subject.gender
        dob = result_item.result.order.aliquot.receive.registered_subject.dob
        reference_datetime = result_item.result.order.aliquot.receive.receive_datetime
        # may pass hiv_status as a kwargs for testing
        hiv_status, is_default_hiv_status = self.get_hiv_status(
            result_item.result.order.aliquot.receive.registered_subject.subject_identifier,
            reference_datetime, **kwargs)
        super(ClinicGradeFlag, self).__init__(
            reference_list,
            test_code,
            gender,
            dob,
            reference_datetime,
            hiv_status,
            is_default_hiv_status, **kwargs)

    def get_lab_tracker_group_name(self):
        """Returns a group name to use when filtering on values in the lab_tracker class.

        See :mode:bhp_lab_tracker"""
        return 'HIV'

    def get_hiv_status(self, subject_identifier, reference_datetime, **kwargs):
        """ """
        hiv_status = kwargs.get('hiv_status', None)
        if not hiv_status:
            subject_identifier, hiv_status, reference_datetime, is_default_hiv_status = lab_tracker.get_value(
                self.get_lab_tracker_group_name(),
                subject_identifier,
                reference_datetime)
        if not hiv_status:
            raise TypeError('hiv_status cannot be None.')
        return (hiv_status, is_default_hiv_status)
