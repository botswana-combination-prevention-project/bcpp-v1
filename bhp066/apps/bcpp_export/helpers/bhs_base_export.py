

class BHSBaseExport(object):

    def __init__(self):
        self.plot_identifier_id = None
        self.household_identifier_id = None
        self.household_member_id = None
        self.registered_subject_id = None
        self._subject_identifier = None

    @property
    def subject_identifier(self):
        """ returns subject identifier from subject_visit """
        pass

    @property
    def plot_identifier(self):
        """ returns plot identifier from household_plot """
        pass

    @property
    def household_identifier(self):
        """ returns HouseholdID from household_household """
        pass

    @property
    def household_member(self):
        """ returns householdMemberID from household_member_subjecthtc """
        pass

    @property
    def registered_subject(self):
        """ returns registered_subject from subject_subjectconsent """
        pass

    @property
    def source_system_create_date(self):
        """ returns source system create date """
        pass

    @property
    def source_system_update_date(self):
        """ returns source lastest update date """
        pass
