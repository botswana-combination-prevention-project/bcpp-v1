from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.lab_tracker.classes import HivLabTracker

from .models import HivTestReview, HivResult


class SubjectHivLabTracker(HivLabTracker):
    subject_type = 'subject'
    trackers = [(HivTestReview, 'recorded_hiv_result', 'hiv_test_date', ),
                (HivResult, 'hiv_result', 'hiv_result_datetime', )]

site_lab_tracker.register(SubjectHivLabTracker)
