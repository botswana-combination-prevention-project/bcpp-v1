import factory

from datetime import datetime, timedelta

from ...models import Survey


class SurveyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Survey

    survey_name = factory.Sequence(lambda n: 'YEAR {0}'.format(n))
    datetime_start = factory.Sequence(lambda n: datetime.today() - timedelta(days=30))
    datetime_end = factory.Sequence(lambda n: datetime.today() + timedelta(days=180))
