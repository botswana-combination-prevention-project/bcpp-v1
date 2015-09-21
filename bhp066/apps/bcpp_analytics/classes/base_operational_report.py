from django.contrib.auth.models import User
from edc.core.bhp_birt_reports.classes import OperationalReportUtilities

from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_survey.models import Survey


class BaseOperationalReport():

    def __init__(self, request):
        self.specimen_info = {}
        self.utilities = OperationalReportUtilities()
        self.date_from = self.utilities.date_format_utility(request.GET.get('date_from', ''), '1960-01-01')
        self.date_to = self.utilities.date_format_utility(request.GET.get('date_to', ''), '2099-12-31')
        self.ra_username = request.GET.get('ra', '')
        self.community = request.GET.get('community', '')
        self.survey = request.GET.get('survey', '')
        self.previous_ra = self.ra_username
        self.previous_community = self.community
        self.previous_survey = self.survey
        self.data_dict = {}
        self.communities = None
        self.ra_usernames = None
        self.surveys = None

    def build_report(self):
        report_data = self.report_data()
        self.configure_filtering()
        return report_data

    def report_data(self):
        """Default returns an exmpty dictionary
           Override in subclass to return a dictionary of actual report data. """
        return {}

    def return_communities(self):
        return self.communities

    def return_ra_usernames(self):
        return self.ra_usernames

    def return_surveys(self):
        return self.surveys

    def configure_filtering(self):
        communities = []
        if (self.previous_community.find('----') == -1) and (not self.previous_community == ''):  # Passing filtered results
            # communities = [community[0].lower() for community in  COMMUNITIES]
            for community in COMMUNITIES:
                if community[0].lower() != self.previous_community:
                    communities.append(community[0])
            communities.insert(0, self.previous_community)
            communities.insert(1, '---------')
        else:
            communities = [community[0].lower() for community in COMMUNITIES]
            communities.insert(0, '---------')
        self.communities = communities
        ra_usernames = []
        if (self.previous_ra.find('----') == -1) and (not self.previous_ra == ''):
            for ra_name in [user.username for user in User.objects.filter(groups__name='field_research_assistant')]:
                if ra_name != self.previous_ra:
                    ra_usernames.append(ra_name)
            ra_usernames.insert(0, self.previous_ra)
            ra_usernames.insert(1, '---------')
        else:
            ra_usernames = [user.username for user in User.objects.filter(groups__name='field_research_assistant')]
            ra_usernames.insert(0, '---------')
        self.ra_usernames = ra_usernames
        surveys = []
        if (self.previous_survey.find('----') == -1) and (not self.previous_survey == ''):
            for slug in [survey.survey_slug for survey in Survey.objects.all()]:
                if slug != self.previous_survey:
                    surveys.append(slug)
            surveys.insert(0, self.previous_survey)
            surveys.insert(1, '---------')
        else:
            surveys = [survey.survey_slug for survey in Survey.objects.all()]
            surveys.insert(0, '---------')
        self.surveys = surveys
