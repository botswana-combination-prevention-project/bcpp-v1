import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import FutureHivTesting


class FutureHivTestingFactory(BaseScheduledModelFactory):
    FACTORY_FOR = FutureHivTesting

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    prefer_hivtest = (('At my home', 'At my home'), ('At a mobile testing tent or vehicle in my neighborhood', 'At a mobile testing tent or vehicle in my neighborhood'), ('At a health facility in my community', 'At a health facility in my community'), ('At a health facility or mobile testing unit outside of my community', 'At a health facility or mobile testing unit outside of my community'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    hiv_test_time = (('Yes, specify', 'Yes, specify:'), ('No, any time of day is fine', 'No, any time of day is fine'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    hiv_test_time_other = factory.Sequence(lambda n: 'hiv_test_time_other{0}'.format(n))
    hiv_test_week = (('Yes, specify', 'Yes, specify:'), ('No, any day of the week is fine', 'No, any day of the week is fine'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    hiv_test_week_other = factory.Sequence(lambda n: 'hiv_test_week_other{0}'.format(n))
    hiv_test_year = (('Yes, specify', 'Yes, specify:'), ('No, any month is fine', 'No, any month is fine'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    hiv_test_year_other = factory.Sequence(lambda n: 'hiv_test_year_other{0}'.format(n))
