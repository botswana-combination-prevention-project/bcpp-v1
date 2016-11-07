from django.contrib.admin import AdminSite


class BcppSurveyAdminSite(AdminSite):
    site_title = 'BCPP Survey'
    site_header = 'BCPP Survey'
    index_title = 'BCPP Survey'
    site_url = '/'
bcpp_survey_admin = BcppSurveyAdminSite(name='bcpp_survey_admin')
