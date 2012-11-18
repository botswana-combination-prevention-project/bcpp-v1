from tracker import LabTracker


class HivLabTracker(LabTracker):
    """Subclasses LabTracker to specialize on tracking HIV results.

    Predefined Class Attributes:
        * resultitem_test_code = ('ELISA', 'RELISA', 'DNAPCR')
        * tracker_test_code = 'HIV'
        * group_name = 'HIV'

    Usage:

    .. code-block:: python

        from bhp_lab_tracker.classes import lab_tracker
        from bhp_lab_tracker.classes import HivLabTracker
        from models import MaternalEligibilityPost, MaternalEligibilityAnte


        class MaternalHivLabTracker(HivLabTracker):
            models = [
                (MaternalEligibilityPost, 'is_hiv_positive', 'registration_datetime'),
                (MaternalEligibilityAnte, 'is_hiv_positive', 'registration_datetime')
                ]
        lab_tracker.register(MaternalHivLabTracker)
    """
    resultitem_test_code = ('ELISA', 'RELISA', 'DNAPCR')
    tracker_test_code = 'HIV'
    group_name = 'HIV'

    def get_display_map_prep(self):
        """Maps HIV result values to single letters for use when displaying the results as a string."""
        return {'A': 'NEG', 'B': 'ACUTE', 'C': 'POSSIBLE ACUTE', 'D': 'IND', 'E': 'POS', 'UNK': '???'}

    def get_default_value(self, *args):
        return 'NEG'
