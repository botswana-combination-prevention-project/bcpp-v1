import factory

from datetime import datetime

from ...models import QualityOfLife


class QualityOfLifeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = QualityOfLife

    report_datetime = datetime.today()
    mobility = (('no problems', u'I have no problems in walking about'), ('slight problems', u'I have slight problems in walking about'), ('moderate problems', u'I have moderate problems in walking about'), ('severe problems', u'I have severe problems in walking about'), ('unable to walk', u'I am unable to walk about'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    self_care = (('no problems', u'I have no problems washing or dressing myself'), ('slight problems', u'I have slight problems washing or dressing myself'), ('moderate problems', u'I have moderate problems washing or dressing myself'), ('severe problems', u'I have severe problems washing or dressing myself'), ('unable to wash', u'I am unable to wash or dress myself'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    activities = (('no problems', u'I have no problems doing my usual activities'), ('slight problems', u'I have slight problems doing my usual activities'), ('moderate problems', u'I have moderate problems doing my usual activities'), ('severe problems', u'I have severe problems doing my usual activities'), ('unable to', u'I am unable to do my usual activities'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    pain = (('no pain', u'I have no pain or discomfort'), ('slight pain', u'I have slight pain or discomfort'), ('moderate pain', u'I have moderate pain or discomfort'), ('severe pain', u'I have severe pain or discomfort'), ('extreme pain', u'I have extreme pain or discomfort'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    anxiety = (('not anxious', u'I am not anxious or depressed'), ('slightly anxious', u'I am slightly anxious or depressed'), ('moderately anxious', u'I am moderately anxious or depressed'), ('severely anxious', u'I am severely anxious or depressed'), ('extremely anxious', u'I am extremely anxious or depressed'), ("Don't want to answer", u"Don't want to answer"))[0][0]
