import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import LabourMarketWages


class LabourMarketWagesFactory(BaseScheduledModelFactory):
    FACTORY_FOR = LabourMarketWages

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    employed = (('government sector', 'Yes, In the government sector'), ('private sector', 'Yes, in the private sector'), ('self-employed working on my own', 'Yes, self-employed working on my own'), ('self-employed with own employees', 'Yes, self-employed with own employees'), ('not working', 'No, not working'), ("Don't want to answer", "Don't want to answer"))[0][0]
    occupation_other = factory.Sequence(lambda n: 'occupation_other{0}'.format(n))
    household_income = (('None', 'None'), ('1-200 pula', '1-200 pula'), ('200-499 pula', '200-499 pula'), ('500-999 pula', '500-999 pula'), ('1000-4999 pula', '1000-4999 pula'), ('5000-10,000 pula', '5000-10,000 pula'), ('10,0000-20,000 pula', '10,0000-20,000 pula'), ('More than 20,000 pula', 'More than 20,000 pula'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other_occupation = (('Studying', 'Studying'), ('Doing housework', 'Doing housework'), ('Looking for work', 'Looking for work'), ('Doing nothing (not looking for paid work)', 'Doing nothing (not looking for paid work)'), ('Retired/old age', 'Retired/old age'), ('Pregnant or recently pregnant', 'Pregnant or recently pregnant'), ('Sick or injured', 'Sick or injured'), ('OTHER', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other_occupation_other = factory.Sequence(lambda n: 'other_occupation_other{0}'.format(n))
    govt_grant = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    weeks_out = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
