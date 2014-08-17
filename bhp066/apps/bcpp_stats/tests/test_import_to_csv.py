from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from django.test import TestCase


class TestImportToCsv(TestCase):
    
header_row = ['a', 'b', 'c', 'd', 'e']
row = [1,2,3,4,5]
    