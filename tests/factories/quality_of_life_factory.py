import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import QualityOfLife


class QualityOfLifeFactory(BaseScheduledModelFactory):
    FACTORY_FOR = QualityOfLife

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    mobility = (('no problems', 'I have no problems in walking about'), ('slight problems', 'I have slight problems in walking about'), ('moderate problems', 'I have moderate problems in walking about'), ('severe problems', 'I have severe problems in walking about'), ('unable to walk', 'I am unable to walk about'), ("Don't want to answer", "Don't want to answer"))[0][0]
    self_care = (('no problems', 'I have no problems washing or dressing myself'), ('slight problems', 'I have slight problems washing or dressing myself'), ('moderate problems', 'I have moderate problems washing or dressing myself'), ('severe problems', 'I have severe problems washing or dressing myself'), ('unable to wash', 'I am unable to wash or dress myself'), ("Don't want to answer", "Don't want to answer"))[0][0]
    activities = (('no problems', 'I have no problems doing my usual activities'), ('slight problems', 'I have slight problems doing my usual activities'), ('moderate problems', 'I have moderate problems doing my usual activities'), ('severe problems', 'I have severe problems doing my usual activities'), ('unable to', 'I am unable to do my usual activities'), ("Don't want to answer", "Don't want to answer"))[0][0]
    pain = (('no pain', 'I have no pain or discomfort'), ('slight pain', 'I have slight pain or discomfort'), ('moderate pain', 'I have moderate pain or discomfort'), ('severe pain', 'I have severe pain or discomfort'), ('extreme pain', 'I have extreme pain or discomfort'), ("Don't want to answer", "Don't want to answer"))[0][0]
    anxiety = (('not anxious', 'I am not anxious or depressed'), ('slightly anxious', 'I am slightly anxious or depressed'), ('moderately anxious', 'I am moderately anxious or depressed'), ('severely anxious', 'I am severely anxious or depressed'), ('extremely anxious', 'I am extremely anxious or depressed'), ("Don't want to answer", "Don't want to answer"))[0][0]
