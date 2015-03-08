from apps.bcpp_survey.models import Survey

from .base_helper import BaseHelper


class Community(BaseHelper):

    def __init__(self, mapper):
        super(Community, self).__init__()
        self.mapper_cls = mapper
        self.mapper = self.mapper_cls()
        self.cpc = mapper.intervention
        self.ecc = not mapper.intervention
        self.community = mapper.map_area
        self.community_id = mapper.map_code
        self.community_code = mapper.map_code
        self.pair = mapper.pair
        for survey in Survey.objects.all():
            survey_dates = mapper.survey_dates[survey.survey_slug]
            setattr(self, '{}_{}'.format("start_date", survey.survey_abbrev.lower()), survey_dates.start_date)
            setattr(self, '{}_{}'.format("full_enrollment_date", survey.survey_abbrev.lower()), survey_dates.full_enrollment_date)
            setattr(self, '{}_{}'.format("end_date", survey.survey_abbrev.lower()), survey_dates.end_date)
            setattr(self, '{}_{}'.format("smc_start_date", survey.survey_abbrev.lower()), survey_dates.smc_start_date)

    def __repr__(self):
        return '{0}({1.mapper_cls!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.community!s}'.format(self)

    @property
    def unique_key(self):
        return self.community

    def customize_for_csv(self):
        super(Community, self).customize_for_csv()
        del self.data['mapper']
        del self.data['mapper_cls']
