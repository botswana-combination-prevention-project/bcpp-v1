from lab_tracker.classes import LabTracker


class HivLabTracker(LabTracker):

    resultitem_test_code = ('ELISA', 'RELISA', 'DNAPCR')
    tracker_test_code = 'HIV'

    def get_display_map_prep(self):
        return {'A': 'NEG', 'B': 'ACUTE', 'C': 'POSSIBLE ACUTE', 'D': 'IND', 'E': 'POS', 'UNK': '???'}
