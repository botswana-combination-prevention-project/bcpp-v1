from bhp_lab_tracker.classes import lab_tracker
from bhp_lab_tracker.classes import HivLabTracker
from models import HivTestReview


class SubjectHivLabTracker(HivLabTracker):
    models = [
        (HivTestReview, 'hivtestdate', 'recordedhivresult', 'verbalhivresult'),
        ]

    def get_default_value(self, group_name, subject_identifier, value_datetime):
        """Returns the a value if none is available."""
        return 'UNKNOWN'

lab_tracker.register(SubjectHivLabTracker)
