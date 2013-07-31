import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import ResidencyMobility


class ResidencyMobilityFactory(BaseUuidModelFactory):
    FACTORY_FOR = ResidencyMobility

    report_datetime = datetime.today()
    length_residence = (('Less than 6 months', u'Less than 6 months'), ('6 months to 12 months', u'6 months to 12 months'), ('1 to 5 years', u'1 to 5 years'), ('More than 5 years', u'More than 5 years'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    forteen_nights = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    intend_residency = (('Yes', u'Yes'), ('No', u'No'), ('not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    nights_away = (('zero', u'Zero nights'), ('1-6 nights', u'1-6 nights'), ('1-2 weeks', u'1-2 weeks'), ('3 weeks to less than 1 month', u'3 weeks to less than 1 month'), ('1-3 months', u'1-3 months'), ('4-6 months', u'4-6 months'), ('more than 6 months', u'more than 6 months'), ('I am not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    cattle_postlands = (('N/A', u'Not Applicable'), ('Farm/lands', u'Farm/lands'), ('Cattle post', u'Cattle post'), ('Other community', u'Other community, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
