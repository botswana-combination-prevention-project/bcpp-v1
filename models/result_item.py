from django.db import models
from lab_test_code.models import TestCode
from lab_result_item.models import BaseResultItem
from lab_reference.classes import ReferenceFlag
from lab_grading.classes import GradeFlag
from bhp_registration.models import RegisteredSubject
from result import Result
from lab_clinic_api.managers import ResultItemManager

class ResultItem(BaseResultItem):

    test_code = models.ForeignKey(TestCode, related_name='test_code_clinic')

    result = models.ForeignKey(Result)
    
    objects = ResultItemManager() 
   
    def __unicode__(self):
        return '%s %s %s' % (unicode(self.result.lab), unicode(self.result), unicode(self.test_code))       

    def save(self, *args, **kwargs):
        

        subject_identifier = self.result.lab.subject_identifier
        if RegisteredSubject.objects.filter(subject_identifier=subject_identifier):
            dob = RegisteredSubject.objects.get(subject_identifier = subject_identifier).dob
            gender = RegisteredSubject.objects.get(subject_identifier = subject_identifier).gender
            
            reference = ReferenceFlag()            
            reference.result_item_value = self.result_item_value
            reference.dob = dob
            reference.gender = gender
            reference.drawn_datetime = self.result.lab.drawn_datetime
            reference.test_code = self.test_code
            if reference.flag:
                self.reference_range = '%s - %s' % (reference.flag['range']['lln'], reference.flag['range']['uln'])
                self.reference_flag = reference.flag['flag']        

            grade = GradeFlag()
            grade.result_item_value = self.result_item_value
            grade.dob = dob
            grade.gender = gender
            grade.drawn_datetime = self.result.lab.drawn_datetime
            grade.test_code = self.test_code
            if grade.flag:
                self.grade_range = '%s - %s' % (grade.flag['range']['lln'], grade.flag['range']['uln'])
                self.grade_flag = grade.flag['flag']        
                
        return super(ResultItem, self).save(*args, **kwargs)

    
    class Meta:
        app_label = "lab_clinic_api"
    
