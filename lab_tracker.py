from bhp_lab_tracker.classes import site_lab_tracker
from bhp_lab_tracker.classes import HivLabTracker
from models import HivTestReview, HivResult


class SubjectHivLabTracker(HivLabTracker):
    trackers = [(HivTestReview, 'recorded_hiv_result', 'hiv_test_date', ),
              (HivResult, 'hiv_result', 'hiv_result_datetime', )]

    def get_default_value(self):
        """Returns the a value if none is available."""
        return 'UNK'

site_lab_tracker.register(SubjectHivLabTracker)
