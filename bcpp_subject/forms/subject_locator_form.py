from django import forms
from bcpp_subject.models import SubjectLocator
from base_subject_model_form import BaseSubjectModelForm


class SubjectLocatorForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(SubjectLocatorForm, self).clean()
        
        """validating home_visits"""
        if cleaned_data.get('home_visit_permission', None) == 'No' and cleaned_data.get('physical_address', None):
            raise forms.ValidationError('If participant has not given permission to make home_visits, do not give physical(home) address details')

        """validating work_place"""
        self.validate_work_place('subject_work_place', cleaned_data)
        self.validate_work_place('subject_work_phone', cleaned_data)

        """validating follow_up"""
        self.validate_follow_up('subject_cell', cleaned_data)
        self.validate_follow_up('subject_cell_alt', cleaned_data)
        self.validate_follow_up('subject_phone', cleaned_data)
        self.validate_follow_up('subject_phone_alt', cleaned_data)
        
        """validating next_of_kin"""
        self.validate_next_of_kin('alt_contact_name', cleaned_data)
        self.validate_next_of_kin('alt_contact_rel', cleaned_data)
        self.validate_next_of_kin('alt_contact_cell', cleaned_data)
        self.validate_next_of_kin('other_alt_contact_cell', cleaned_data)
        self.validate_next_of_kin('alt_contact_tel', cleaned_data)
       
        return cleaned_data
    
    
    def validate_follow_up(self, field, cleaned_data):
        msg = 'If participant has not given permission for follow-up, do not give follow-up details'
        self.validate_dependent_fields('may_follow_up', field,cleaned_data, msg)
    
    def validate_next_of_kin(self, field, cleaned_data):
        msg ='If participant has not given permission to contact next_of_kin, do not give next_of_kin details'
        self.validate_dependent_fields('has_alt_contact', field,cleaned_data, msg)
        
    def validate_work_place(self, field, cleaned_data):
        msg ='If participant has not given permission to contact him/her at work, do not give work details'
        self.validate_dependent_fields('may_call_work', field,cleaned_data, msg)
    
    def validate_dependent_fields(self,master_field, sub_field, cleaned_data, msg):
        if cleaned_data.get(master_field, None) == 'No' and cleaned_data.get(sub_field, None):
            raise forms.ValidationError(msg)


    class Meta:
        model = SubjectLocator
