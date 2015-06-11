import socket
import re


class ReplacementHelper(object):
    """Check replaceable household and plots, then replace them.

    Attributes involved:

        plot.replaced_by: plot identifier of the new replacement plot
        plot.replaces: plot or household identifier of the old plot
            or household being replaced.
        plot.htc
        household.replaced_by: plot identifier of the new replacement plot

        plot.status  # user
        plot.plot_identifier  # save
        plot.dispatched_to  # dispatch
        household.household_identifier  # save
        household_structure.enumerated  # post_save
        household_structure.refused_enumeration  # post_save
        household_structure.no_informant  # post_save
        household_structure.failed_enumeration   # post_save
        household_structure.failed_enumeration_attempts   # post_save
        household_structure.household
        household_structure.eligible_members   # post_save
        household_structure.visit_attempts
    """

    def __init__(self, plot=None, household_structure=None):
        """Sets household_structure, household and plot.

        The household_structure takes precedent."""
        self._household_structure = None
        self._plot = None
        self._replacement_reason = None

    def update_site_tracker(self):
        pass


    def update_producer_tracker(self):
        pass


    def tracked_value(self):
        pass


    def producer_online(self):
        pass
