import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import ResidencyMobility


class ResidencyMobilityFactory(BaseScheduledModelFactory):
    FACTORY_FOR = ResidencyMobility

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    length_residence = (('Less than 6 months', 'Less than 6 months'), ('6 months to 12 months', '6 months to 12 months'), ('1 to 5 years', '1 to 5 years'), ('More than 5 years', 'More than 5 years'), ("Don't want to answer", "Don't want to answer"))[0][0]
    forteen_nights = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    intend_residency = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    nights_away = (('zero', 'Zero nights'), ('1-6 nights', '1-6 nights'), ('1-2 weeks', '1-2 weeks'), ('3 weeks to less than 1 month', '3 weeks to less than 1 month'), ('1-3 months', '1-3 months'), ('4-6 months', '4-6 months'), ('more than 6 months', 'more than 6 months'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    cattle_postlands = (('N/A', 'Not Applicable'), ('Farm/lands', 'Farm/lands'), ('Cattle post', 'Cattle post'), ('Other community', 'Other community, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
