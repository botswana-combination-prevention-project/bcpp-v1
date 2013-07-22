import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import BloodDraw


class BloodDrawFactory(BaseUuidModelFactory):
    FACTORY_FOR = BloodDraw

    report_datetime = datetime.today()
    draw_date = datetime.today()
    is_blood_drawn = (('Yes', 'Yes'), ('No', 'No'))[0][0]
