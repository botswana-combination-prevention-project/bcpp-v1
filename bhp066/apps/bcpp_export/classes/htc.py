from edc.constants import NO

from apps.bcpp_household_member.models import SubjectHtc

from .base import Base
from .household import Household
from .household_member import HouseholdMember
from .plot import Plot
from .survey import Survey


class Htc(Base):
    def __init__(self, household_member, check_errors=False):
        super(Htc, self).__init__()
        self.errors = {}
        self.household_member = HouseholdMember(household_member)
        self.update_member()
        try:
            plot = self.household_member.household_structure.household.plot
            household = self.household_member.household_structure.household
        except AttributeError:
            plot = None
            household = None
        self.plot = Plot(plot)
        self.household = Household(household)
        self.update_plot()
        self.update_household()
        self.update_survey()
        self.update_htc()
        if check_errors:
            self.data_errors

    def __repr__(self):
        return 'Htc({0.household_member!r})'.format(self)

    def __str__(self):
        return '{0.household_member!r}'.format(self)

    def customize_for_csv(self):
        """Customizes attribute self.data dictionary."""
        super(Htc, self).customize_for_csv()
        self.data['registered_subject'] = self.data['registered_subject'].registration_identifier
        self.data['household_member'] = self.data['household_member'].internal_identifier
        del self.data['plot']
        del self.data['household']
        del self.data['survey']
        del self.data['subject_htc']

    def update_htc(self):
        try:
            self.subject_htc = SubjectHtc.objects.get(
                household_member__internal_identifier=self.household_member.internal_identifier)
            self.report_date = self.subject_htc.report_datetime.date()
            self.offered = self.subject_htc.offered
            self.accepted = self.subject_htc.accepted
            self.tracking_identifier = self.subject_htc.tracking_identifier
            if self.accepted == NO:
                self.refusal_reason = self.subject_htc.refusal_reason
            else:
                self.refusal_reason = None
            self.referred = self.subject_htc.referred
            self.referral_clinic = self.subject_htc.referral_clinic
        except SubjectHtc.DoesNotExist:
            self.subject_htc = None
            self.report_date = None
            self.offered = None
            self.accepted = None
            self.tracking_identifier = None
            self.refusal_reason = None
            self.referred = None
            self.referral_clinic = None

    def update_plot(self):
        self.plot_identifier = self.plot.plot_identifier
        self.community = self.plot.community

    def update_household(self):
        self.household_identifier = self.household.household_identifier

    def update_survey(self):
        self.survey = Survey(self.community)
        for attr, value in self.survey.__dict__.iteritems():
            setattr(self, attr, value)

    def update_member(self):
        """Set attributes from the HouseholdMember instance."""
        attrs = [
            ('first_name', 'first_name'),
            ('initials', 'initials'),
            ('age_in_years', 'age_in_years'),
            ('gender', 'gender'),
            ('study_resident', 'study_resident'),
            ('enumeration_first_date', 'enumeration_first_date'),
            ('enumeration_last_date', 'enumeration_last_date'),
            ('internal_identifier', 'internal_identifier'),
            ('registered_subject', 'registered_subject'),
            ]
        for attr in attrs:
            setattr(self, attr[1], getattr(self.household_member, attr[0]))
