import factory

from datetime import datetime

from edc.constants import NOT_APPLICABLE

from ...models import ResidencyMobility


class ResidencyMobilityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ResidencyMobility

    report_datetime = datetime.today()
    length_residence = (('Less than 6 months', u'Less than 6 months'), ('6 months to 12 months', u'6 months to 12 months'), ('1 to 5 years', u'1 to 5 years'), ('More than 5 years', u'More than 5 years'), ('not_answering', u"Don't want to answer"))[0][0]
    permanent_resident = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    intend_residency = (('Yes', u'Yes'), ('No', u'No'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[1][0]
    nights_away = (('zero', u'Zero nights'), ('1-6 nights', u'1-6 nights'), ('1-2 weeks', u'1-2 weeks'), ('3 weeks to less than 1 month', u'3 weeks to less than 1 month'), ('1-3 months', u'1-3 months'), ('4-6 months', u'4-6 months'), ('more than 6 months', u'more than 6 months'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]
    cattle_postlands = ((NOT_APPLICABLE, u'Not Applicable'), ('Farm/lands', u'Farm/lands'), ('Cattle post', u'Cattle post'), ('Other community', u'Other community, specify:'), ('not_answering', u"Don't want to answer"))[0][0]
