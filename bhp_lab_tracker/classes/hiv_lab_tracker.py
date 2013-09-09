from tracker import LabTracker


class HivLabTracker(LabTracker):
    """Subclasses LabTracker to specialize on tracking HIV results.

    Predefined Class Attributes:
        * tracked_test_codes = ('ELISA', 'RELISA', 'DNAPCR')
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
    tracked_test_codes = ('ELISA', 'RELISA', 'DNAPCR', 'HIV')
    group_name = 'HIV'

    def get_display_map_prep(self):
        """Maps HIV result values to single letters for use when displaying the results as a string."""
        return {'A': 'NEG', 'B': 'ACUTE', 'C': 'POSSIBLE ACUTE', 'D': 'IND', 'E': 'POS', 'UNK': 'UNK'}

    def get_default_value(self):
        """Returns the a value if none is available."""
        return 'UNK'
