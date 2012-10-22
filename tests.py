'''
Created on Oct 19, 2012

@author: sirone
'''
from django.utils import unittest
from models import ResultItem
from lab_flag.classes import Flag
from bhp_registration.models import RegisteredSubject
from lab_grading.classes import GradeFlag
from lab_grading import utils
from lab_result_item.classes import ResultItemFlag


class ResultItemTestCase(unittest.TestCase):

    test_data = ResultItem.objects.exclude(grade_flag__isnull=True)[:20]

    def __init__(self):
        pass

    # def setUp(self):
        # self.item = ResultItem.objects.create(subject_identifier="xxx", receive_identifier="xxxxx")

#    def print_index(self,index):
#        print self.test_data[index];

    def test_print_no_returned(self):
        return self.test_data.count()

    def test_grade_flag(self):
        for result in self.test_data:
            if RegisteredSubject.objects.filter(subject_identifier=result.subject_identifier).count() == 1:
                # print RegisteredSubject.objects.filter(subject_identifier=result.subject_identifier).count()
                subjects = RegisteredSubject.objects.filter(subject_identifier=result.subject_identifier)
                subject = subjects[0]
            flag_args = {'result_value': result.result_item_value_as_float,
                         'test_code': result.test_code,
                         'datetime_drawn': subject.registration_datetime,
                         'dob': subject.dob,
                         'gender': subject.gender,
                         'hiv_status': subject.hiv_status}
            test_flag = utils.calculate_grade(**flag_args)
            #result_item = ResultItem.objects.create()
            #reference_range, reference_flag, grade_range, grade_flag = ResultItemFlag().calculate(result_item)

            # self.assertEqual(test_flag, result.grade_flag)
            if test_flag != result.grade_flag:
                print "FAILED, NewFlag=" + str(test_flag) + " OldFlag=" + str(result.grade_flag) + ", Identifier=" + str(result.subject_identifier)
            print "--------------------------------------------------------------------"
    # if __name__ == '__main__':
        # unittest.main()
