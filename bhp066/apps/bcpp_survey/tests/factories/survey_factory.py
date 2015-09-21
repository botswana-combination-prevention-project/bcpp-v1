import factory

from datetime import datetime, timedelta

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import Survey


class SurveyFactory(BaseUuidModelFactory):
    FACTORY_FOR = Survey

    survey_name = factory.Sequence(lambda n: 'YEAR {0}'.format(n))
    datetime_start = factory.Sequence(lambda n: datetime.today() - timedelta(days=30))
    datetime_end = factory.Sequence(lambda n: datetime.today() + timedelta(days=180))
